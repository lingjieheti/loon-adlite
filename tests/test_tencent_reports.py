"""Exercise exact Tencent ad reporting hosts and neighboring user-facing services."""
import unittest
from urllib.parse import urlsplit

from test_suite import ROOT, Rewrite, read_sections


class TencentReports(unittest.TestCase):
    def test_ad_receivers_are_blocked_without_decryption(self):
        reports = (
            "https://rpt.gdt.qq.com/creative_view?example=1",
            "https://sdkreport.e.qq.com/link_event",
            "https://t.gdt.qq.com/conv/sdk/spa/conv",
        )
        for name in ("iPad-AdSuite.lpx", "iPad-AdLite.lpx"):
            sections = read_sections(ROOT / name)
            blocked = set(sections["rule"])
            decrypted = {h.strip() for line in sections.get("mitm", ())
                         for h in line.partition("=")[2].split(",")}
            for url in reports:
                host = urlsplit(url).hostname
                with self.subTest(plugin=name, host=host):
                    self.assertIn(f"DOMAIN,{host},REJECT", blocked)
                    self.assertNotIn(host, decrypted)
                    for other in (host.partition(".")[2], "sub." + host, host + ".example.org"):
                        self.assertNotIn(f"DOMAIN,{other},REJECT", blocked)

    def test_messaging_login_payments_and_link_navigation_stay_available(self):
        urls = (
            "https://open.weixin.qq.com/connect/oauth2/authorize",
            "https://mp.weixin.qq.com/s/example", "https://long.weixin.qq.com/",
            "https://weixin110.qq.com/security/readtemplate", "https://support.weixin.qq.com/",
            "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi",
            "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb",
            "https://ptlogin2.qq.com/ptqrlogin", "https://im.qq.com/",
            "https://qzone.qq.com/", "https://h5.qzone.qq.com/report/native",
            "https://push.qq.com/", "https://url.cn/example",
            "https://c.gdt.qq.com/gdt_trace_a.fcg", "https://v.gdt.qq.com/gdt_stats.fcg",
            "https://livew.l.qq.com/livemsg?pf=H5&ad=1",
        )
        suite = read_sections(ROOT / "iPad-AdSuite.lpx")
        blocked = {line.split(",")[1] for line in suite["rule"]}
        rewrites = [Rewrite.parse(line) for line in suite["rewrite"]]
        for url in urls:
            with self.subTest(url=url):
                self.assertNotIn(urlsplit(url).hostname, blocked)
                self.assertFalse(any(rewrite.matches(url) for rewrite in rewrites))
