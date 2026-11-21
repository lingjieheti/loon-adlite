"""Offline Safari helper tests. Set WEB_ADS_TEST_BROWSER=webkit to run in WebKit."""

from contextlib import contextmanager
import os
from pathlib import Path
import re
import unittest

from playwright.sync_api import Error, sync_playwright


SOURCE = Path(__file__).resolve().parents[1] / "web" / "pornhub.user.js"
ORIGIN = "https://www.pornhub.com"
ADS = """
    <aside id="side" class="sideAds">Sidebar placement</aside>
    <section id="mobileContainer"><p id="intro">Introduction</p>
      <div id="mobile" class="watchpageAd">Mobile placement</div></section>
    <ins id="slot" class="adsbytrafficjunky">Network placement</ins>
    <a id="paid" href="https://ads.trafficjunky.net/click">Advertiser</a>
"""
CONTENT = """
    <video id="video" controls width="160" height="90"></video>
    <section id="age"><button id="confirm">Confirm age</button></section>
    <section id="consent"><button id="decline">Decline optional cookies</button></section>
    <a id="login" href="/login">Log in</a>
    <a id="external" href="https://example.org/article">Article</a>
    <a id="similar" href="https://ads.trafficjunky.net.example.org/path">Different host</a>
    <a id="query" href="/help?target=https://ads.trafficjunky.net/">Help</a>
    <a id="cdn" href="https://dl.phncdn.com/pics/example">Image</a>
    <div id="outside" class="watchpageAd">Outside the mobile layout</div>
    <ins id="edit">Editorial correction</ins>
"""
HTML = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<script>
window.clicks = [];
document.addEventListener("click", event => {
    event.preventDefault();
    window.clicks.push(event.target.id);
}, true);
</script>"""
PLACEMENTS = ("side", "mobile", "slot", "paid")


class WebAdsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SOURCE.read_text(encoding="utf-8")
        playwright = sync_playwright().start()
        cls.addClassCleanup(playwright.stop)
        if os.getenv("WEB_ADS_TEST_BROWSER") == "webkit":
            cls.browser = playwright.webkit.launch()
        elif os.getenv("CHROME_BIN"):
            cls.browser = playwright.chromium.launch(executable_path=os.environ["CHROME_BIN"])
        else:
            try:
                cls.browser = playwright.chromium.launch(channel="chrome")
            except Error:
                cls.browser = playwright.chromium.launch()
        cls.addClassCleanup(cls.browser.close)

    @contextmanager
    def fixture(self, markup, origin=ORIGIN, child=False):
        url = origin + "/fixture"
        documents = {url: markup}
        if child:
            documents[origin + "/child"] = ADS
        errors = []
        unexpected = []
        with self.browser.new_context(service_workers="block") as context:
            def serve(route):
                request = route.request
                if request.resource_type == "document" and request.url in documents:
                    route.fulfill(content_type="text/html; charset=utf-8",
                                  body=HTML + documents[request.url] + "</body></html>")
                else:
                    unexpected.append(request.url)
                    route.abort()

            # WebKit renders native video controls with in-memory blob URLs.
            context.route(re.compile(r"^https?://"), serve)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(url)
            page.add_script_tag(content=self.script)
            yield page
            self.assertEqual(page.evaluate("[localStorage.length, sessionStorage.length, document.cookie]"),
                             [0, 0, ""])
            self.assertEqual(unexpected, [])
            self.assertEqual(errors, [])

    def assert_placements(self, frame, *, visible):
        for name in PLACEMENTS:
            with self.subTest(placement=name):
                self.assertEqual(frame.locator("#" + name).is_visible(), visible)

    def test_ads_hidden_and_ordinary_content_usable(self):
        for origin in (ORIGIN, "https://pornhub.com", "https://m.pornhub.com"):
            with self.subTest(origin=origin), self.fixture(ADS + CONTENT, origin) as page:
                self.assert_placements(page, visible=False)
                for name in ("intro", "video", "age", "consent", "external", "similar", "query", "cdn", "outside", "edit"):
                    self.assertTrue(page.locator("#" + name).is_visible(), name)
                self.assertEqual(page.evaluate("clicks"), [])
                self.assertEqual(page.locator("video").evaluate(
                    "v => [v.controls, v.paused, v.currentTime, v.playbackRate, v.muted]"),
                    [True, True, 0, 1, False])
                for name in ("confirm", "decline", "login", "external"):
                    page.locator("#" + name).click(timeout=2000)
                self.assertEqual(page.evaluate("clicks"), ["confirm", "decline", "login", "external"])

    def test_dynamic_ads_are_hidden_and_reinjection_is_idempotent(self):
        with self.fixture(CONTENT) as page:
            page.evaluate("html => document.body.insertAdjacentHTML('beforeend', html)", ADS)
            self.assert_placements(page, visible=False)
            styles = page.locator("style").count()
            page.add_script_tag(content=self.script)
            self.assertEqual(page.locator("style").count(), styles)
            self.assertTrue(page.locator("#external").is_visible())

    def test_unrelated_lookalike_and_http_origins_untouched(self):
        for origin in ("https://example.org", "https://notpornhub.com",
                       "https://pornhub.com.example.org", "http://www.pornhub.com"):
            with self.subTest(origin=origin), self.fixture(ADS, origin) as page:
                self.assert_placements(page, visible=True)
                self.assertEqual(page.locator("style").count(), 0)

    def test_matching_site_inside_an_iframe_remains_untouched(self):
        with self.fixture(ADS + '<iframe name="child" src="/child"></iframe>', child=True) as page:
            frame = page.frame(name="child")
            frame.add_script_tag(content=self.script)
            self.assert_placements(page, visible=False)
            self.assert_placements(frame, visible=True)
            self.assertEqual(frame.locator("style").count(), 0)


if __name__ == "__main__":
    unittest.main()
