"""Run the userscript against offline browser fixtures: python tests/checkin_browser.py"""

import os
from datetime import datetime, timezone
from pathlib import Path
import unittest
from urllib.parse import urldefrag

from playwright.sync_api import Error, sync_playwright


SCRIPT = (Path(__file__).resolve().parents[1] / "checkin" / "daily.user.js").read_text(encoding="utf-8")
JD = "https://bean.jd.com/myJingBean/list"
SMZDM = "https://www.smzdm.com/"
FRAGMENT = "#loon-checkin"
JD_BUTTON = "https://img11.360buyimg.com/dl/jfs/t1/90191/32/54493/5536/6722f8bcF77a507b7/c5688a27a125651b.png"
JD_ACCOUNT = '<li id="ttbar-login"><a class="nickname" href="https://home.jd.com/">测试账户</a></li>'
JD_LOGIN = '<li id="ttbar-login"><a class="link-login" href="/login">你好，请登录</a></li>'
SMZDM_ACCOUNT = '<div class="app-header__mine"><img class="app-header__avatar" alt=""></div>'
SMZDM_LOGIN = '<div class="app-header__guest">请登录</div>'
FIXED_TIME = datetime(2026, 11, 21, 16, 30, tzinfo=timezone.utc)


def day(text, classes="node", amount=None):
    reward = f'<div class="txt_wrap"><span class="txt_num">{amount}</span></div>' if amount else ""
    return f'<div class="{classes}">{reward}<div class="text">{text}</div></div>'


PENDING = day("连签2天", "node sign-in") + day("今天", "node continuity-no-sign") + day("明天")
FALLBACK = day("今天") + day("明天") + day("后天")
FINISHED = day("昨天", "node sign-in") + day("连签2天", "node sign-in") + day("明天")


def jd_page(nodes=PENDING, account=JD_ACCOUNT, extra="", button=None):
    if button is None:
        button = f'<div class="btn" data-action="sign"><img class="img" src="{JD_BUTTON}" alt=""></div>'
    return f"""{account}<div id="mybean-sign"><div id="bean-sign-component">
        <div class="header" data-action="promotion"><div class="title">签到领京豆</div></div>
        <div class="progress">{nodes}</div>{button}{extra}</div></div>
        <button data-action="shopping">一键领取</button>"""


def smzdm_page(account=SMZDM_ACCOUNT, state="", text="签到领奖"):
    return f"""<header class="app-header">{account}
        <div class="header-checkin {state}"><button class="header-checkin-button"
        type="button" aria-busy="false" data-action="sign"><span aria-live="polite">{text}</span>
        </button></div></header><button data-action="shopping">签到领奖</button>"""


SHELL = """<!doctype html><html lang="zh"><meta charset="utf-8">
<style>img {display:inline-block;width:30px;height:26px} .btn {width:110px;height:38px}</style>
<body><script>
window.clicks = [];
document.addEventListener('click', event => {
  event.preventDefault();
  window.clicks.push(event.target.closest('[data-action]')?.dataset.action || 'unexpected');
}, true);
</script>"""


class CheckinBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        playwright = sync_playwright().start()
        cls.addClassCleanup(playwright.stop)
        executable = os.environ.get("CHROME_BIN")
        if executable:
            cls.browser = playwright.chromium.launch(executable_path=executable)
        else:
            try:
                cls.browser = playwright.chromium.launch(channel="chrome")
            except Error:
                cls.browser = playwright.chromium.launch()
        cls.addClassCleanup(cls.browser.close)

    def verify(self, base, body, *, path=None, fragment=FRAGMENT, clicks=0, repeat=False, init=None):
        document = path or base
        key = "loon-adlite:" + ("jd" if base == JD else "smzdm") + ":attempt-date"
        unexpected = []
        errors = []
        with self.browser.new_context(service_workers="block") as ctx:
            def intercept(route):
                request = route.request
                if request.resource_type == "document" and urldefrag(request.url).url == document:
                    route.fulfill(content_type="text/html; charset=utf-8", body=SHELL + body + "</body></html>")
                elif request.resource_type == "image" and request.url == JD_BUTTON:
                    route.fulfill(content_type="image/svg+xml", body='<svg xmlns="http://www.w3.org/2000/svg" width="560" height="108"/>')
                else:
                    unexpected.append(request.url)
                    route.abort()

            ctx.route("**/*", intercept)
            page = ctx.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.clock.install(time=FIXED_TIME)
            page.goto(document + fragment, wait_until="load")
            if init:
                page.evaluate(init)

            def run():
                page.add_script_tag(content=SCRIPT)
                page.clock.fast_forward(12000)
                # Queue behind any lock request made by the script before observing its result.
                page.evaluate("key => navigator.locks?.request(key, () => {})", key)
                return page.evaluate("window.clicks")

            self.assertEqual(run(), ["sign"] * clicks)
            self.assertEqual(
                page.evaluate("key => localStorage.getItem(key)", key),
                "2026-11-22" if clicks else None,
            )
            if repeat:
                page.reload(wait_until="load")
                self.assertEqual(run(), [])
            self.assertEqual(errors, [])
            self.assertEqual(unexpected, [])

    def test_jd_clicks_once_across_reloads(self):
        self.verify(JD, jd_page(), clicks=1, repeat=True)

    def test_offscreen_signed_in_card_is_rechecked_after_scrolling(self):
        self.verify(JD, '<div style="height:200vh"></div>' + jd_page(), clicks=1)

    def test_jd_today_reward_and_yesterdays_sign(self):
        with self.subTest("reward on first node"):
            self.verify(JD, jd_page(day("今天可领", "reward_node", "+3") + day("明天") + day("后天")), clicks=1)
        with self.subTest("historical signed label"):
            nodes = day("已签到", "node sign-in") + day("连签2天", "node sign-in") + day("今天可领", "reward_node", "+2")
            self.verify(JD, jd_page(nodes), clicks=1)

    def test_jd_leaves_unclear_or_ineligible_pages_untouched(self):
        cases = {
            "completed": jd_page(FINISHED),
            "fallback calendar": jd_page(FALLBACK),
            "unloaded calendar": jd_page(""),
            "login": jd_page(account=JD_LOGIN),
            "signup guide": jd_page(extra='<div class="guide">欢迎来签到领京豆</div>'),
            "official reward dialog": jd_page(extra='<div class="mask"><div class="success">签到成功，恭喜获得京豆</div></div>'),
            "shopping button inside sign card": jd_page(button='<a href="/shop" class="btn" data-action="shopping">签到</a>'),
            "ambiguous action": jd_page(button='<div class="btn" data-action="shopping">领取优惠券</div>'),
            "duplicate today": jd_page(PENDING + day("今天")),
            "overlay": jd_page() + '<div style="position:fixed;inset:0;z-index:100"></div>',
        }
        for name, body in cases.items():
            with self.subTest(name):
                self.verify(JD, body)

    def test_smzdm_account_and_status(self):
        self.verify(SMZDM, smzdm_page(), clicks=1, repeat=True)
        for name, body in (
            ("already signed", smzdm_page(state="header-checkin--done", text="已签到")),
            ("guest", smzdm_page(account=SMZDM_LOGIN)),
            ("shopping instead of sign-in", smzdm_page(text="领取优惠券")),
            ("verification", smzdm_page() + '<dialog open>请完成验证</dialog>'),
        ):
            with self.subTest(name):
                self.verify(SMZDM, body)

    def test_missing_deduplication_capabilities(self):
        for name, failure in (
            ("no Web Locks", "() => Object.defineProperty(navigator, 'locks', {value: undefined})"),
            ("storage read-only", "() => { Storage.prototype.setItem = () => { throw new Error('read-only'); }; }"),
        ):
            with self.subTest(name):
                self.verify(JD, jd_page(), init=failure)

    def test_ordinary_urls_and_other_pages_are_inert(self):
        for base, body in ((JD, jd_page()), (SMZDM, smzdm_page())):
            for name, path, fragment in (
                ("ordinary visit", base, ""),
                ("another fragment", base, "#offers"),
                ("another page", base.rstrip("/") + "/other", FRAGMENT),
                ("query parameter", base + "?from=ad", FRAGMENT),
            ):
                with self.subTest(base=base, situation=name):
                    self.verify(base, body, path=path, fragment=fragment)


if __name__ == "__main__":
    unittest.main()
