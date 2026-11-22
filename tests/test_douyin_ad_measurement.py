"""Offline regressions for the Pangle log hosts and Douyin's shared content services."""

import unittest
from urllib.parse import urlsplit

import test_suite as shared


REPORT_HOSTS = {"log-api.pangolin-sdk-toutiao.com", "log-api.pangolin-sdk-toutiao-b.com"}
# Public video with verified MP4 metadata; the feed envelope below is constructed for this test.
# https://github.com/yt-dlp/yt-dlp/blob/91361cca6ed4313d4ff5516cf150512da6209ba2/yt_dlp/extractor/tiktok.py#L1373-L1388
VIDEO_ID = "6961737553342991651"
VIDEO_URL = f"https://www.douyin.com/video/{VIDEO_ID}"
STREAM_URL = "https://v11-colds.douyinvod.com/example/video/tos/cn/example/?mime_type=video_mp4"


class DouyinAdMeasurement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shared.AdSuite.setUpClass()
        cls.rules = shared.AdSuite.rules
        cls.jq = shared.AdSuite.jq

    matches = shared.AdSuite.matches
    check_body = shared.AdSuite.check_body

    def test_only_exact_log_hosts_blocked_without_decryption(self):
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx"):
            sections = shared.read_sections(shared.ROOT / name)
            rules = set(sections["rule"])
            intercepted = {host.strip() for line in sections.get("mitm", ())
                           for host in line.partition("=")[2].split(",")}
            for host in REPORT_HOSTS:
                with self.subTest(plugin=name, host=host):
                    self.assertIn(f"DOMAIN,{host},REJECT", rules)
                    self.assertNotIn(host, intercepted)
                    parent = host.partition(".")[2]
                    for neighbor in (parent, f"sub.{host}", f"{host}.example.org"):
                        self.assertNotIn(f"DOMAIN,{neighbor},REJECT", rules)

    def test_stream_share_live_product_and_detail_bypass_blocking(self):
        urls = (
            VIDEO_URL, STREAM_URL, "https://v.douyin.com/L4NpDJ6/",
            f"https://www.iesdouyin.com/share/video/{VIDEO_ID}/",
            f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={VIDEO_ID}",
            "https://webcast.amemv.com/webcast/room/check_alive/",
            "https://live.douyin.com/webcast/room/web/enter/",
            "https://haohuo.jinritemai.com/views/product/item2?id=3514453298386183303",
        )
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx"):
            blocked = set(shared.read_sections(shared.ROOT / name)["rule"])
            for url in urls:
                with self.subTest(plugin=name, url=url):
                    self.assertNotIn(f"DOMAIN,{urlsplit(url).hostname},REJECT", blocked)
                    if name == "iPad-AdSuite.lpx":
                        self.assertFalse(self.matches(url))

    def test_shared_feed_keeps_public_video_and_its_playback_metadata(self):
        organic = {
            "aweme_id": VIDEO_ID, "aweme_type": 0, "is_ads": False, "share_url": VIDEO_URL,
            "video": {"duration": 19000, "play_addr": {"url_list": [STREAM_URL]}},
        }
        page = {"status_code": 0, "aweme_list": [organic], "has_more": 1}
        mixed = {**page, "aweme_list": [{"is_ads": True}, organic]}
        for host, version in (("api3-core-c.amemv.com", 1), ("api3-normal-c.amemv.com", 2)):
            url = f"https://{host}/aweme/v{version}/feed/"
            with self.subTest(url=url):
                for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx"):
                    self.assertNotIn(f"DOMAIN,{host},REJECT", shared.read_sections(shared.ROOT / name)["rule"])
                self.check_body(url, mixed, page)
                self.check_body(url, page, page)
                self.assertFalse(self.matches(f"{url}?aweme_id={VIDEO_ID}"))


if __name__ == "__main__":
    unittest.main()
