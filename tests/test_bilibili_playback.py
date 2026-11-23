"""Offline checks of Bilibili playback traffic against the three shipped plugins."""

import unittest
from urllib.parse import urlsplit

from test_suite import ROOT, Rewrite, read_sections


SUBSCRIPTIONS = ("iPad-AdLite.lpx", "iPad-InlineAds.lpx", "iPad-AdSuite.lpx")
# Public sample IDs. Signed playback query strings and media URLs are not needed for these checks.
VIDEOS = (("BV17x411w7KC", 279786), ("BV1GJ411x7h7", 137649199), ("BV1xx411c7mD", 62131))
PLAYBACK_URLS = (
    "https://api.bilibili.com/pgc/player/web/v2/playurl?ep_id=267851&cid=125463156",
    "https://api.bilibili.com/pugv/player/web/playurl?ep_id=1",
    "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id=6",
    "https://api.bilibili.tv/intl/gateway/web/playurl",
    "https://grpc.biliapi.net/bilibili.app.playerunite.v1.Player/PlayViewUnite",
    "https://grpc.biliapi.net/bilibili.app.playurl.v1.PlayURL/PlayView",
    # Observed CDN hostnames paired with synthetic paths; real media URLs expire.
    "https://cn-hbyc-ct-01-05.bilivideo.com/video/example.m4s",
    "https://cn-hbyc-ct-01-01.bilivideo.com/audio/example.m4s",
    "https://upos-sz-estghw.bilivideo.com/video/example.mp4",
    "https://upos-sz-mirrorcos.bilivideo.com/audio/example.m4s",
    "https://example-node.edge.mountaintoys.cn/video/example.mp4",
    "https://d1--cn-gotcha104.bilivideo.com/live/example.m3u8",
)


class BilibiliPlayback(unittest.TestCase):
    def setUp(self):
        self.plugins = {}
        for name in SUBSCRIPTIONS:
            sections = read_sections(ROOT / name)
            blocked = {rule.split(",")[1] for rule in sections.get("rule", [])}
            decrypted = {host.strip() for line in sections.get("mitm", [])
                         for host in line.partition("=")[2].split(",")}
            rewrites = [Rewrite.parse(line) for line in sections.get("rewrite", [])]
            self.plugins[name] = blocked, decrypted, rewrites

    def test_playback_hosts_and_media_bypass_the_plugin(self):
        urls = list(PLAYBACK_URLS)
        for bvid, cid in VIDEOS:
            urls.extend((
                f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}",
                f"https://api.bilibili.com/x/player/wbi/playurl?bvid={bvid}&cid={cid}",
            ))
        for name, (blocked, decrypted, rewrites) in self.plugins.items():
            for url in urls:
                with self.subTest(plugin=name, url=url):
                    host = urlsplit(url).hostname
                    self.assertNotIn(host, blocked)
                    self.assertNotIn(host, decrypted)
                    options = {"method": "POST", "mime": "application/grpc"} if host == "grpc.biliapi.net" else {}
                    self.assertFalse(any(rule.matches(url, **options) for rule in rewrites))

    def test_app_feed_and_splash_are_separate_from_playback(self):
        host = "app.bilibili.com"
        for name, (blocked, decrypted, rewrites) in self.plugins.items():
            with self.subTest(plugin=name):
                app_filters = name != "iPad-AdLite.lpx"
                self.assertNotIn(host, blocked)
                self.assertEqual(host in decrypted, app_filters)
                for path in ("/x/v2/feed/index", "/x/v2/splash/list"):
                    matches = [rule for rule in rewrites if rule.matches(f"https://{host}{path}")]
                    self.assertEqual(len(matches), int(app_filters))
                related = f"https://{host}/x/v2/feed/index/relate/story"
                self.assertFalse(any(rule.matches(related) for rule in rewrites))
                for path in ("/bilibili.app.playurl.v1.PlayURL/PlayView",
                             "/bilibili.cheese.gateway.player.v1.PlayURL/PlayView"):
                    url = f"https://{host}{path}"
                    self.assertFalse(any(rule.matches(url, method="POST", mime="application/grpc")
                                         for rule in rewrites), url)
