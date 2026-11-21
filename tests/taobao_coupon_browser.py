"""Offline browser checks for the selected Taobao shop coupon, including WebKit."""

from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
from time import monotonic
import unittest
from urllib.parse import urldefrag

from playwright.sync_api import Error, sync_playwright


SCRIPT = Path(__file__).resolve().parents[1] / "checkin" / "taobao-coupon.user.js"
BASE = "https://market.m.taobao.com/apps/aliyx/coupon/detail.html"
SELLER, ACTIVITY = "987654321", "0123456789abcdef0123456789abcdef"
QUERY = f"?wh_weex=true&sellerId={SELLER}&activityId={ACTIVITY}&"
MARKER = f"#loon-coupon={SELLER}.{ACTIVITY}"
START = datetime(2026, 11, 21, 3, tzinfo=timezone.utc)
ASSET = "https://gw.alicdn.com/tps/"
HEADER = "TB1k1tEOXXXXXb8apXXXXXXXXXX-750-6.png"
FOOTER = "TB1Xd8DOXXXXXcpaFXXXXXXXXXX-750-6.png"
SHOP = "TB1IrlUOXXXXXcfaXXXXXXXXXXX-178-164.png"
PRODUCT = "TB1XCihOXXXXXaCXVXXXXXXXXXX-178-178.png"
BUTTON = '<div role="button" disabled="false"><span>确认领取</span></div>'
SHELL = """<!doctype html><html lang="zh-CN"><meta charset="utf-8"><body>
<script>window.actions = []; document.addEventListener('click', e => {
 e.preventDefault(); actions.push(e.target.closest('[role=button]')?.textContent || 'unexpected');
}, true);</script>"""


def coupon(*, title="测试店铺优惠券", icon=SHOP, amount="5", terms="满 30 使用",
           period="有效期 2026.11.01 00:00-2026.12.01 23:59", action=BUTTON, extra=""):
    # This element order was observed by rendering the published 0.1.2 Rax view
    # with synthetic display data and a stub claim handler. All offer details below are fictional.
    return f"""<div class="rax-scrollview" data-spm-protocol="i"><div><div><div>
      <div><div><img src="{ASSET}{HEADER}"><img src="{ASSET}{FOOTER}"><span>{title}</span>
      <div><span></span><span>{period}</span><span></span></div><img src="{ASSET}{icon}">
      <div><span>￥</span><span>{amount}</span></div><span>{terms} </span></div></div>
      {extra}<div>{action}</div></div></div></div></div>"""


class TaobaoCouponBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SCRIPT.read_text(encoding="utf-8")
        p = sync_playwright().start()
        cls.addClassCleanup(p.stop)
        cls.ipad = p.devices["iPad (gen 7)"]
        if os.getenv("COUPON_TEST_BROWSER") == "webkit":
            cls.browser = p.webkit.launch()
        elif os.getenv("CHROME_BIN"):
            cls.browser = p.chromium.launch(executable_path=os.environ["CHROME_BIN"])
        else:
            try:
                cls.browser = p.chromium.launch(channel="chrome")
            except Error:
                cls.browser = p.chromium.launch()
        cls.addClassCleanup(cls.browser.close)

    @contextmanager
    def fixture(self, body, url=BASE + QUERY + MARKER):
        errors, unexpected = [], []
        with self.browser.new_context(**self.ipad, service_workers="block") as context:
            def serve(route):
                request = route.request
                if request.resource_type == "document" and request.url == urldefrag(url).url:
                    route.fulfill(body=SHELL + body + "</body></html>", content_type="text/html; charset=utf-8")
                elif request.resource_type == "image" and request.url in {
                    ASSET + name for name in (HEADER, FOOTER, SHOP, PRODUCT)
                }:
                    route.fulfill(content_type="image/svg+xml", body='<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"/>')
                else:
                    unexpected.append(request.url)
                    route.abort()
            context.route("**/*", serve)
            context.on("page", lambda p: p.on("pageerror", lambda e: errors.append(str(e))))
            page = context.new_page()
            page.clock.install(time=START)
            page.goto(url)
            yield page
            self.assertEqual(errors, [])
            self.assertEqual(unexpected, [])

    def observe(self, page, count):
        if count:
            page.wait_for_function("n => actions.length >= n", arg=count, timeout=3000)
        page.clock.fast_forward(12000)
        page.evaluate("() => new Promise(resolve => setTimeout(resolve, 30))")
        self.assertEqual(page.evaluate("actions"), ["确认领取"] * count)

    def test_selected_coupon_once_after_render_and_reload(self):
        with self.fixture('<div id="loading"></div>') as page:
            page.add_script_tag(content=self.source)
            page.locator("#loading").evaluate("(e, html) => e.outerHTML = html", coupon())
            page.clock.fast_forward(500)
            self.observe(page, 1)
            stored = page.evaluate("JSON.stringify(localStorage) + JSON.stringify(sessionStorage)")
            for value in (SELLER, ACTIVITY, BASE):
                self.assertNotIn(value, stored)
            page.reload()
            page.locator("#loading").evaluate("(e, html) => e.outerHTML = html", coupon())
            page.add_script_tag(content=self.source)
            self.observe(page, 0)

    def test_two_tabs_share_one_attempt(self):
        with self.fixture(coupon(terms="无条件使用")) as first:
            second = first.context.new_page()
            second.clock.install(time=START)
            second.goto(first.url)
            for page in (first, second):
                page.evaluate("""src => {
                    Object.defineProperty(document, 'visibilityState', {get: () => 'visible'});
                    Object.defineProperty(document, 'hidden', {get: () => false});
                    window.signal = new BroadcastChannel('taobao-offline-test');
                    signal.onmessage = () => (0, eval)(src);
                }""", self.source)
            first.evaluate("() => new BroadcastChannel('taobao-offline-test').postMessage('go')")
            deadline = monotonic() + 3
            while monotonic() < deadline:
                if first.evaluate("actions.length") + second.evaluate("actions.length"):
                    break
                first.wait_for_timeout(30)
            for page in (first, second):
                page.clock.fast_forward(12000)
                page.evaluate("() => new Promise(resolve => setTimeout(resolve, 30))")
            self.assertEqual(first.evaluate("actions") + second.evaluate("actions"), ["确认领取"])

    def test_marker_must_match_official_url(self):
        for url in (BASE + QUERY, BASE + QUERY.rstrip("&") + MARKER, BASE + QUERY + "&" + MARKER,
                    BASE + QUERY + "#loon-coupon",
                    BASE + QUERY + MARKER.replace(SELLER, "123"),
                    BASE + QUERY + MARKER.replace(ACTIVITY, "b" * 32),
                    BASE + QUERY + "redirect=other&" + MARKER,
                    BASE + QUERY + "sellerId=" + SELLER + "&" + MARKER,
                    BASE.replace("market.m.taobao.com", "market.m.taobao.com.example.org") + QUERY + MARKER,
                    BASE.replace("detail.html", "list.html") + QUERY + MARKER):
            with self.subTest(url=url), self.fixture(coupon(), url) as page:
                page.add_script_tag(content=self.source)
                self.observe(page, 0)

    def test_coupon_card_and_action_must_match_official_structure(self):
        samples = {
            "ordinary-looking label on product icon": coupon(icon=PRODUCT),
            "wrong type": coupon(title="测试商品优惠券"),
            "fee": coupon(terms="支付1元领取"),
            "follow requirement": coupon(extra="<span>关注店铺后领取</span>"),
            "expired": coupon(period="有效期 2026.01.01 00:00-2026.10.01 00:00"),
            "two buttons": coupon(action=BUTTON + BUTTON),
            "disabled action": coupon(action=BUTTON.replace('disabled="false"', 'disabled="true"')),
            "bare disabled attribute": coupon(action=BUTTON.replace('disabled="false"', 'disabled')),
            "redirect": coupon(action=f'<a href="/pay">{BUTTON}</a>'),
            "wallet action": coupon(action=BUTTON.replace("确认领取", "查看领到的券")),
            "login dialog": coupon() + '<dialog open>请先登录</dialog>',
            "obscured button": coupon() + '<div style="position:fixed;inset:0;z-index:5"></div>',
            "unrelated matching text": f"<main>店铺优惠券，满 30 使用{BUTTON}</main>",
        }
        for name, body in samples.items():
            with self.subTest(name=name), self.fixture(body) as page:
                page.add_script_tag(content=self.source)
                self.observe(page, 0)

    def test_hidden_page_and_iframe_are_inert(self):
        with self.fixture(coupon()) as page:
            page.evaluate("""() => {Object.defineProperty(document, 'visibilityState', {get: () => 'hidden'});
                Object.defineProperty(document, 'hidden', {get: () => true});}""")
            page.add_script_tag(content=self.source)
            self.observe(page, 0)
        with self.fixture(coupon()) as page:
            page.evaluate("() => document.body.append(document.createElement('iframe'))")
            frame = page.frames[1]
            frame.goto(page.url)
            frame.add_script_tag(content=self.source)
            page.clock.fast_forward(12000)
            self.assertEqual(frame.evaluate("actions"), [])


if __name__ == "__main__":
    unittest.main()
