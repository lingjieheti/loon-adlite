"""Verify that domestic app ad hosts stay separate from adjacent content and account services."""
import unittest

from test_suite import ROOT, read_sections


# Reviewed ad hosts paired with ordinary services from the same app or publisher.
APP_HOSTS = (
    (("video-dsp.pddpic.com",), ("img.pddpic.com", "video.pddpic.com", "mobile.yangkeduo.com")),
    (("ad.api.moji.com", "adlaunch.moji.com"), ("wwwapi.moji.com", "api.moji.com")),
    (("adx.hupu.com",), ("nba.hupu.com", "m.hupu.com")),
    (("advertise.baicizhan.com", "advertise.baicizhan.org"),
     ("passport.baicizhan.com", "reading.baicizhan.com")),
    (("adpai.thepaper.cn",), ("image.thepaper.cn", "audios.thepaper.cn")),
    (("cdn-new-ad.wtzw.com",), ("cdn.qimao.com", "zuozhe.qimao.com")),
    (("api-ad-product.huxiu.com",), ("www.huxiu.com",)),
    (("adse.ximalaya.com", "adse.wsa.ximalaya.com"), ("api.ximalaya.com", "audio.xmcdn.com")),
    (("ads.service.kugou.com", "adserviceretry.kugou.com"), ("gateway.kugou.com", "webfs.yun.kugou.com")),
    (("ad.qingting.fm", "ad-cdn.qingting.fm"), ("api.open.qingting.fm", "gw-main-prd.qingting.fm")),
    (("api.newad.ifeng.com",), ("news.ifeng.com", "i.ifeng.com")),
    (("impservice.dictapp.youdao.com", "dsp-impr2.youdao.com"), ("dict.youdao.com", "openapi.youdao.com")),
    (("bj.imp.voiceads.cn",), ("imeclient.openspeech.cn", "www.xfyun.cn")),
)


class DomesticDomainRules(unittest.TestCase):
    def test_both_subscriptions_block_only_the_named_ad_hosts(self):
        for name in ("iPad-AdLite.lpx", "iPad-AdSuite.lpx"):
            sections = read_sections(ROOT / name)
            domains = {line.split(",")[1] for line in sections["rule"]}
            intercepted = {h.strip() for line in sections.get("mitm", [])
                           for h in line.partition("=")[2].split(",")}
            for ads, keep in APP_HOSTS:
                with self.subTest(plugin=name, ads=ads):
                    self.assertTrue(set(ads) <= domains)
                    self.assertTrue(intercepted.isdisjoint((*ads, *keep)))
                    self.assertTrue(domains.isdisjoint(keep))
                    for host in ads:
                        parent = host.split(".", 1)[1]
                        self.assertNotIn(parent, domains)
                        self.assertNotIn("example." + host, domains)
            self.assertFalse({"p.kuaidi100.com", "t-dsp.pinduoduo.com"} & intercepted)
            self.assertTrue(domains.isdisjoint({"www.autohome.com.cn", "www.58.com",
                                                "da.mgtv.com", "t-dsp.pinduoduo.com"}))
