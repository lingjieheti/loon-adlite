"""Offline regressions for one explicitly selected JD coupon. Set COUPON_TEST_BROWSER=webkit for WebKit."""

from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
from time import monotonic
import unittest
from urllib.parse import urldefrag

from playwright.sync_api import Error, sync_playwright


SCRIPT = Path(__file__).resolve().parents[1] / "checkin" / "jd-coupon.user.js"
BASE = "https://coupon.m.jd.com/coupons/show.action"
OPT_IN = "#loon-coupon"
BY_KEY = "?key=SyntheticFree&roleId=123"
BY_LINK = "?linkKey=SyntheticSingle"
NOW = datetime(2026, 11, 21, 3, 0, tzinfo=timezone.utc)
SHELL = """<!doctype html><html lang="zh-CN"><meta charset="utf-8"><body>
<script>window.actions = []; document.addEventListener("click", e => {
  e.preventDefault(); window.actions.push(e.target.closest("[data-action]")?.dataset.action || "unexpected");
}, true);</script>"""
AMOUNT = '<p class="money"><em>¥</em><strong>5</strong></p>'
DISCOUNT = '<p class="discount-money"><strong>9</strong><span>折</span></p>'
BUTTON = '<div class="btn" data-action="claim">立即领取</div>'


def coupon(value=AMOUNT, rule="满100元可用", scope="限购指定商品", extra="", button=BUTTON):
    # Compact fixture of JD's public receive-coupon-m component. Values and IDs are synthetic.
    return f"""<div id="root"><div class="wx_wrap"><div class="mjd-coupon"><div class="coupon-box">
        <div class="coupon-value"><div class="coupon-content">{value}<p class="rule">{rule}</p></div></div>
        <div class="coupon-info"><div class="info-content"><p class="use-rule line2">{scope}</p></div></div>
        {extra}</div></div><div class="coupon-btns">{button}</div></div></div>"""


class CouponBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        p = sync_playwright().start()
        cls.addClassCleanup(p.stop)
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
    def fixture(self, body, url=BASE + BY_KEY + OPT_IN):
        unexpected, errors = [], []
        document = urldefrag(url).url
        with self.browser.new_context(viewport={"width":820, "height":1180}, service_workers="block") as context:
            def serve(route):
                if route.request.url == document and route.request.resource_type == "document":
                    route.fulfill(content_type="text/html; charset=utf-8", body=SHELL + body + "</body></html>")
                else:
                    unexpected.append(route.request.url)
                    route.abort()
            context.route("**/*", serve)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.clock.install(time=NOW)
            page.goto(url)
            yield page
            self.assertEqual(unexpected, [])
            self.assertEqual(errors, [])

    def observe(self, page, count):
        if count:
            page.wait_for_function("n => actions.length >= n", arg=count, timeout=3000)
        page.clock.fast_forward(11000)
        # Let outstanding digest/lock callbacks and already scheduled page tasks finish.
        page.evaluate("() => new Promise(resolve => setTimeout(resolve, 30))")
        self.assertEqual(page.evaluate("actions"), ["claim"] * count)

    def test_selected_free_coupon_only_once_across_reload(self):
        for query, value in ((BY_KEY, AMOUNT), (BY_LINK, DISCOUNT)):
            with self.subTest(query=query), self.fixture(coupon(value=value), BASE + query + OPT_IN) as page:
                page.add_script_tag(content=self.script)
                self.observe(page, 1)
                page.reload()
                page.add_script_tag(content=self.script)
                self.observe(page, 0)
                stored = page.evaluate("JSON.stringify(localStorage) + JSON.stringify(sessionStorage)")
                for identifier in ("SyntheticFree", "SyntheticSingle", BASE):
                    self.assertNotIn(identifier, stored)

    def test_late_render_and_simultaneous_injections(self):
        with self.fixture('<div id="loading">加载中</div>') as page:
            # Two script instances can encounter the same late-rendered coupon in one turn.
            page.evaluate("src => { for (let i=0; i<2; ++i) (0,eval)(src); }", self.script)
            page.locator("#loading").evaluate("(e, html) => e.outerHTML = html", coupon())
            page.clock.fast_forward(350)
            self.observe(page, 1)

    def test_another_selected_coupon_and_the_next_beijing_day(self):
        with self.fixture(coupon()) as page:
            page.add_script_tag(content=self.script)
            self.observe(page, 1)
            page.evaluate("url => history.replaceState(null, '', url)", BASE + BY_LINK + OPT_IN)
            page.add_script_tag(content=self.script)
            self.observe(page, 2)
            page.clock.set_system_time(datetime(2026, 11, 21, 16, 1, tzinfo=timezone.utc))
            page.add_script_tag(content=self.script)
            self.observe(page, 3)

    def test_two_visible_tabs_share_one_daily_attempt(self):
        with self.fixture(coupon()) as first:
            second = first.context.new_page()
            second.goto(first.url)
            for page in (first, second):
                page.evaluate("""src => {
                    Object.defineProperty(document, 'visibilityState', {get: () => 'visible'});
                    Object.defineProperty(document, 'hidden', {get: () => false});
                    document.hasFocus = () => true;
                    window.startSignal = new BroadcastChannel('offline-coupon-test');
                    startSignal.onmessage = () => (0,eval)(src);
                }""", self.script)
            first.evaluate("() => new BroadcastChannel('offline-coupon-test').postMessage('go')")
            deadline = monotonic() + 3
            while monotonic() < deadline:
                if first.evaluate("actions.length") + second.evaluate("actions.length") > 0:
                    break
                first.wait_for_timeout(30)
            first.clock.fast_forward(11000)
            second.evaluate("() => new Promise(resolve => setTimeout(resolve, 30))")
            self.assertEqual(first.evaluate("actions") + second.evaluate("actions"), ["claim"])

    def test_unselected_or_ambiguous_urls_are_inert(self):
        cases = [BASE + BY_KEY, BASE + BY_KEY + "#offers", BASE + OPT_IN,
                 BASE + "?roleId=123" + OPT_IN, BASE + BY_KEY + "&key=Duplicate" + OPT_IN,
                 BASE + BY_KEY + "&returnUrl=other" + OPT_IN, BASE + BY_KEY + "&linkKey=Other" + OPT_IN,
                 BASE + "?linkKey=" + "A" * 201 + OPT_IN,
                 BASE.replace("coupon.m.jd.com", "coupon.m.jd.com.example.org") + BY_KEY + OPT_IN,
                 BASE + "/other" + BY_KEY + OPT_IN]
        # Chromium upgrades this HSTS domain before routing the offline HTTP document.
        if self.browser.browser_type.name == "webkit":
            cases.append(BASE.replace("https:", "http:") + BY_KEY + OPT_IN)
        for url in cases:
            with self.subTest(url=url), self.fixture(coupon(), url) as page:
                page.add_script_tag(content=self.script)
                self.observe(page, 0)

    def test_ineligible_cards_and_official_expired_dialog_are_inert(self):
        expired = ('<div class="mod_alert_v2 show fixed"><p>您关注的活动已结束<br>请看看其他活动哦！！</p>'
                   '<p class="btns"><a class="btn btn_1" data-action="confirm">确定</a></p></div>')
        cases = {
            "expired guest landing": '<div id="root"><div class="wx_wrap"></div></div>' + expired,
            "stale card behind dialog": coupon() + expired,
            "follow": coupon(extra='<div class="fans">关注店铺后领取</div>'),
            "paid": coupon(rule="支付1元领取"),
            "fee in offer scope": coupon(scope="限购指定商品，每张券收费1元"),
            "paid coupon": coupon(scope="有价券专区，1元购券"),
            "exchange": coupon(rule="兑换需100京豆"),
            "member": coupon(extra='<i class="mark-vip"></i>'),
            "already received": coupon(button=BUTTON.replace("立即领取", "立即使用")),
            "upsell": coupon(button=BUTTON.replace("立即领取", "膨胀领取")),
            "ambiguous actions": coupon(button=BUTTON + BUTTON),
            "no amount": coupon(value=""),
            "ordinary button outside coupon": '<button data-action="unrelated">立即领取</button>',
        }
        for name, body in cases.items():
            with self.subTest(state=name), self.fixture(body) as page:
                page.add_script_tag(content=self.script)
                self.observe(page, 0)

    def test_not_visible_and_embedded_pages_are_inert(self):
        with self.fixture(coupon()) as page:
            page.evaluate("""() => { Object.defineProperty(document, 'visibilityState', {get: () => 'hidden'});
                Object.defineProperty(document, 'hidden', {get: () => true}); }""")
            page.add_script_tag(content=self.script)
            self.observe(page, 0)
        with self.fixture(coupon()) as page:
            page.evaluate("() => document.body.append(document.createElement('iframe'))")
            frame = page.frames[1]
            frame.goto(BASE + BY_KEY + OPT_IN)
            frame.add_script_tag(content=self.script)
            page.clock.fast_forward(11000)
            self.assertEqual(frame.evaluate("actions"), [])


if __name__ == "__main__":
    unittest.main()
