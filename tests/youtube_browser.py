"""Offline YouTube userscript regressions. Set YOUTUBE_TEST_BROWSER=webkit to test WebKit."""

from contextlib import contextmanager
import os
from pathlib import Path
import unittest

from playwright.sync_api import Error, sync_playwright


SOURCE = Path(__file__).resolve().parents[1] / "youtube" / "youtube.user.js"
DESKTOP = "https://www.youtube.com"
MOBILE = "https://m.youtube.com"
WATCH = "/watch?v=a1B2c3D4e5F"
BUTTON = '<button type="button" class="ytp-skip-ad-button" id="skip" aria-label="Skip ad"><span>Skip ad</span></button>'
SHELL = """<!doctype html><meta charset="utf-8"><style>
  button {min-height:34px} #movie_player {width:320px;position:relative} video {width:32px;height:20px}
  ytd-ad-slot-renderer, ytm-promoted-sparkles-web-renderer {display:block}
</style><body><script>
  window.clicked = [];
  document.addEventListener('click', e => {
    e.preventDefault();
    window.clicked.push(e.target.closest('button,a')?.id || 'unexpected');
  }, true);
</script>"""


def player(button=BUTTON, ad=True):
    state = " ad-showing" if ad else ""
    return f"""<div id="movie_player" class="html5-video-player{state}">
        <video class="video-stream html5-main-video"></video>
        <div class="video-ads ytp-ad-module"><div class="ytp-ad-player-overlay">
          <div class="ytp-ad-skip-button-container ytp-ad-skip-button-container-detached">
            <div class="ytp-skip-ad">{button}</div>
          </div>
        </div></div><button id="next" class="ytp-next-button">Next video</button>
      </div>"""


def settle(page):
    page.evaluate("() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))")


def navigate(page, path):
    page.evaluate("""path => {
        document.dispatchEvent(new Event('yt-navigate-start', {bubbles:true}));
        history.pushState(null, '', path);
        document.dispatchEvent(new Event('yt-navigate-finish', {bubbles:true}));
    }""", path)
    settle(page)


class YouTubeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SOURCE.read_text(encoding="utf-8")
        p = sync_playwright().start()
        cls.addClassCleanup(p.stop)
        if os.getenv("YOUTUBE_TEST_BROWSER") == "webkit":
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
    def fixture(self, markup, url=DESKTOP + WATCH, before=""):
        errors = []
        requests = []
        with self.browser.new_context(service_workers="block") as context:
            def intercept(route):
                if route.request.resource_type == "document" and route.request.url == url:
                    route.fulfill(content_type="text/html; charset=utf-8", body=SHELL + markup + "</body>")
                else:
                    requests.append(route.request.url)
                    route.abort()

            context.route("**/*", intercept)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(url)
            if before:
                page.evaluate(before)
            page.add_script_tag(content=self.script)
            settle(page)
            yield page
            self.assertEqual(errors, [])
            self.assertEqual(requests, [])
            self.assertEqual(page.evaluate("[localStorage.length, sessionStorage.length, document.cookie]"), [0, 0, ""])

    def test_watch_clicks_ready_control_once_without_touching_media(self):
        for host in (DESKTOP, MOBILE):
            with self.subTest(host=host), self.fixture(player(), host + WATCH) as page:
                page.evaluate("document.querySelector('#skip span').textContent = '跳过广告'")
                settle(page)
                self.assertEqual(page.evaluate("clicked"), ["skip"])
                self.assertEqual(page.locator("video").evaluate("v => [v.currentTime,v.playbackRate,v.muted,v.volume]"), [0, 1, False, 1])

    def test_countdown_and_reused_control(self):
        disabled = BUTTON.replace('<button ', '<button disabled ')
        with self.fixture(player(disabled)) as page:
            self.assertEqual(page.evaluate("clicked"), [])
            page.locator("#skip").evaluate("b => b.disabled = false")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])
            page.locator("#skip").evaluate("b => b.hidden = true")
            settle(page)
            page.locator("#skip").evaluate("b => b.hidden = false")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip", "skip"])

    def test_mobile_control_without_player_id_waits_for_its_label(self):
        body = """<div class="html5-video-player ad-showing"><div class="ytp-skip-ad" style="pointer-events:none">
            <button id="skip" class="ytp-skip-ad-button" type="button" style="pointer-events:auto" aria-label="5 秒后跳过">
              <div class="ytp-skip-ad-button__text">تخطّي الإعلان بعد ٥</div>
            </button></div></div>"""
        with self.fixture(body, MOBILE + WATCH) as page:
            self.assertEqual(page.evaluate("clicked"), [])
            label = page.locator(".ytp-skip-ad-button__text")
            page.locator("#skip").evaluate("e => e.setAttribute('aria-label', '略過廣告')")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), [])  # The visible text still shows a countdown.
            label.evaluate("e => e.firstChild.data = '略過廣告'")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])
            label.evaluate("e => e.firstChild.data = 'スキップ'")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])

    def test_no_action_on_unrelated_or_unavailable_controls(self):
        cases = {
            "ordinary video": player(ad=False),
            "advertiser link and next video": player('<a id="visit" href="/watch?v=a1B2c3D4e5F">Skip ad</a>'),
            "lookalike outside player": player("") + BUTTON,
            "lookalike outside ad module": player("").replace('<button id="next"', BUTTON + '<button id="next"'),
            "hidden": player(BUTTON.replace("<button ", "<button hidden ")),
            "transparent ancestor": player(f'<div style="opacity:0">{BUTTON}</div>'),
            "aria disabled": player(BUTTON.replace("<button ", '<button aria-disabled="true" ')),
            "ambiguous buttons": player(BUTTON + BUTTON.replace('id="skip"', 'id="another"')),
            "covered": player() + '<div style="position:fixed;inset:0;background:#fff;z-index:99"></div>',
        }
        for case, body in cases.items():
            with self.subTest(case=case), self.fixture(body) as page:
                self.assertEqual(page.evaluate("clicked"), [])

    def test_home_to_watch_and_back_without_reload(self):
        with self.fixture(player(), DESKTOP + "/") as page:
            self.assertEqual(page.evaluate("clicked"), [])
            navigate(page, WATCH)
            self.assertEqual(page.evaluate("clicked"), ["skip"])
            navigate(page, "/shorts/a1B2c3D4e5F")
            page.locator("#skip").evaluate("b => b.replaceWith(b.cloneNode(true))")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])

    def test_embed_shorts_and_incomplete_watch_links_are_inert(self):
        for origin, path in (
            (DESKTOP, "/embed/a1B2c3D4e5F"), (MOBILE, "/shorts/a1B2c3D4e5F"),
            (DESKTOP, "/watch"), (DESKTOP, "/watch?v="), ("https://www.youtube.com.example.test", WATCH),
        ):
            with self.subTest(origin=origin, path=path), self.fixture(player(), origin + path) as page:
                self.assertEqual(page.evaluate("clicked"), [])

    def test_hidden_page_defers_work_and_iframe_never_clicks(self):
        before = """() => {
            window.background = true;
            Object.defineProperty(document, 'hidden', {get: () => window.background});
            Object.defineProperty(document, 'visibilityState', {get: () => window.background ? 'hidden' : 'visible'});
        }"""
        with self.fixture(player(), before=before) as page:
            self.assertEqual(page.evaluate("clicked"), [])
            page.evaluate("() => {window.background = false; document.dispatchEvent(new Event('visibilitychange'))}")
            settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])
            for hidden in (True, False):
                page.evaluate("""hidden => {
                    window.background = hidden;
                    document.dispatchEvent(new Event('visibilitychange'));
                }""", hidden)
                settle(page)
            self.assertEqual(page.evaluate("clicked"), ["skip"])
        with self.fixture('<iframe></iframe>') as page:
            frame = page.frames[1]
            frame.goto(DESKTOP + WATCH)
            frame.set_content(SHELL + player() + "</body>")
            frame.add_script_tag(content=self.script)
            settle(frame)
            self.assertEqual(frame.evaluate("clicked"), [])

    def test_only_standalone_feed_ads_are_hidden_on_their_own_routes(self):
        cases = (
            (DESKTOP, "/", '<div id="contents"><ytd-rich-item-renderer id="card"><div id="content">'
             '<ytd-ad-slot-renderer id="ad">Ad</ytd-ad-slot-renderer><span id="story">Video</span>'
             '</div></ytd-rich-item-renderer></div>'),
            (DESKTOP, "/results?search_query=music", '<ytd-item-section-renderer id="card"><div class="ytd-item-section-renderer">'
             '<ytd-ad-slot-renderer id="ad">Ad</ytd-ad-slot-renderer><span id="story">Video</span>'
             '</div></ytd-item-section-renderer>'),
            (MOBILE, "/", '<ytm-rich-item-renderer id="card"><ad-slot-renderer id="ad">Ad</ad-slot-renderer>'
             '<span id="story">Video</span></ytm-rich-item-renderer>'),
            (MOBILE, "/results?search_query=music", '<lazy-list id="card"><ad-slot-renderer id="ad">Ad</ad-slot-renderer>'
             '<span id="story">Video</span></lazy-list>'),
        )
        for host, path, body in cases:
            with self.subTest(host=host, path=path), self.fixture(body, host + path) as page:
                self.assertTrue(page.locator("#ad").is_hidden())
                self.assertTrue(page.locator("#story").is_visible())
                self.assertEqual(page.locator("#card").count(), 1)
                page.evaluate("""() => {
                    const independent = document.querySelector('#ad').cloneNode(true);
                    independent.id = 'unrelated';
                    document.body.append(independent);
                }""")
                self.assertTrue(page.locator("#unrelated").is_visible())
                navigate(page, WATCH)
                self.assertTrue(page.locator("#ad").is_visible())
                self.assertEqual(page.evaluate("clicked"), [])


if __name__ == "__main__":
    unittest.main()
