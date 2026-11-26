# 常用 App 去广告的覆盖范围

iPhone 和 iPad 共用[懒人版订阅](README.md#安装)。插件有 77 条固定的精确域名规则，本次上游同步另收录 5 个主机，合计 82 个。域名拦截无需证书。懒人版另有 41 条原生复写，并列出 34 个需要在本机进行 HTTPS 解密的完整主机名。域名数会随审核后的上游更新而变化。同一款 App 可能从多个渠道投放广告，规则数量不能换算为拦截率。[当前订阅内容](iPad-AdSuite.lpx)

## 网页广告

- **Google 视频直播和点播**。部分播放器需要从 `pubads.g.doubleclick.net` 取得 HLS 或 DASH 播放清单。轻量版和懒人版均允许访问这个共用主机，也允许它承载的广告请求。随节目合流的广告仍可能播放。[Google 播放清单地址](https://support.google.com/admanager/answer/7299051?hl=en) · [公开测试流](https://developers.google.com/ad-manager/dynamic-ad-insertion/streams) · [EasyList 的直播放行规则](https://github.com/easylist/easylist/blob/27076a68237ad6a4eebb00b190439473c926ea03/easylist/easylist_allowlist.txt#L530)

- **网页竞价广告**。Loon 拦截 PubMatic、Criteo 和 TripleLift 的指定竞价主机。新增的 `tlx.3lift.com` 用于 Prebid 的浏览器竞价，AdAway 也收录了这个完整主机名。同一广告位可能向其他广告商询价。[PubMatic](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/pubmaticBidAdapter.js#L25) · [Criteo](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/criteoBidAdapter.js#L27) · [TripleLift](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/tripleliftBidAdapter.js#L10) · [AdAway](https://github.com/AdAway/adaway.github.io/blob/f39ba0a523564447dfa94e40327c1a14c02304dc/hosts.txt#L81)
- **百度联盟展示广告**。AMP 的百度广告组件从 `dup.baidustatic.com` 加载广告脚本，EasyList China 也将其列为广告主机，因此插件精确拦截该主机。另一个广告主机 `cpro.baidustatic.com` 有四个网站的指定脚本放行例外，因此留给能识别来源网页和路径的浏览器过滤器处理。[AMP 百度广告组件](https://github.com/ampproject/amphtml/blob/29d4f68e5a1017ed5d63e3086b219b4b25a41332/ads/vendors/baidu.js#L16-L35) · [EasyList China 主机规则](https://github.com/easylist/easylistchina/blob/7efab892b13dc99ed81f1995887a9c0f79510362/easylistchina.txt#L7928) · [网站例外](https://github.com/easylist/easylistchina/blob/7efab892b13dc99ed81f1995887a9c0f79510362/easylistchina.txt#L15828-L15829)
- **Pornhub 网页**。Loon 另拦 `a.adtng.com` 和 `ads.trafficjunky.net`。页面内嵌广告、同源投放及拼入正片的片段仍可能出现。这两条全局规则也会影响其他网站。EasyList 允许 `hanime.tv` 的部分嵌入框架访问 `adtng.com/get/`；若框架实际使用 `a.adtng.com`，Loon 的域名拦截仍会生效。尚未验证该站的实际播放影响。[域名清单](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/category-ads#L74-L81) · [TrafficJunky 广告位](https://www.trafficjunky.com/advertiser/ad-formats) · [EasyList 框架例外](https://github.com/easylist/easylist/blob/68a1b6472a6954f713eb62f3919ca7b8301f5ab4/easylist/easylist_allowlist.txt#L489)
- **Safari 页面清理**。可选助手通过站点专用 CSS 隐藏部分侧栏、移动播放页广告容器及明确标记的投放元素。它可以清掉部分广告占位，无法识别已经拼进视频的广告。该功能需用支持用户脚本的扩展单独安装。[网页助手](web/pornhub.user.js)

离线测试核对上述广告主机的精确匹配，并检查主域、共享 CDN、相似主机和正常视频路径。当前缺少这些广告位在 iPad 上的实机命中记录，也未测量启用前后的吞吐量。[域名回归测试](tests/test_suite.py)

**开源规则如何搭配**。2026-11-21 比对的 HaGeZi Multi LIGHT 快照含 91,706 个不同域名。项目更新前的 43 个广告主机中，21 个与该清单完全相同，另有 11 个落在它列出的父域之下。这个数字反映清单重叠程度。Loon 订阅只保留选定的完整主机；需要处理普通网页里的横幅和空位时，可以在 Safari 里选用 AdGuard 的基础和中文过滤器，让浏览器应用页面规则和网站例外。[对比用的插件版本](https://github.com/lingjieheti/loon-adlite/blob/ae273c03c32c98f7dafe938aed4e05fdcfd9045a/iPad-AdLite.lpx) · [HaGeZi 固定快照](https://github.com/hagezi/dns-blocklists/blob/6033fe872ee360ff34da5a9e826558030938fc7e/wildcard/light-onlydomains.txt) · [Safari 可选设置](web/README.md#普通网页仍有横幅或广告空位)

## 微信与 QQ 广告监测

**微信公众文章。** 懒人版复用 `mp.weixin.qq.com` 的本机 HTTPS 解密。规则依据第三方仓库留存的旧版微信文章页面脚本，只在指定路径和参数匹配时，在设备上直接应答。

| 匹配的请求 | 处理方式 |
| --- | --- |
| `/mp/ad_report` 的 `action=see_report` | 对带广告标识的已知像素请求在本机返回小图片，涵盖滚动至广告特定位置及广告可见 500、1000、2000 毫秒的上报。[可见位置与时长](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/index42f400.js#L1617-L1627) |
| `/mp/advertisement_report` 的 `action=extra_report` | 对已识别的附加上报在本机返回空 JSON 对象。这条路径用于记录点击时间或递交累积的曝光时长。[点击计时](https://github.com/stellarkey/912_project/blob/688e74dabb40b4ffd1ca47a9d8a72495c77b6ddb/1%20%E6%8B%9B%E7%94%9F%E4%BF%A1%E6%81%AF/%21%E6%8B%9B%E7%94%9F%E6%A6%82%E5%86%B5/%E3%80%90%E9%95%9C%E5%83%8F%E3%80%91%E7%8E%8B%E9%81%93%E5%9C%A8%E7%BA%BF/%E7%8E%8B%E9%81%93%E5%9C%A8%E7%BA%BF_files/report42f400.js#L227-L242) · [曝光计时](https://github.com/stellarkey/912_project/blob/688e74dabb40b4ffd1ca47a9d8a72495c77b6ddb/1%20%E6%8B%9B%E7%94%9F%E4%BF%A1%E6%81%AF/%21%E6%8B%9B%E7%94%9F%E6%A6%82%E5%86%B5/%E3%80%90%E9%95%9C%E5%83%8F%E3%80%91%E7%8E%8B%E9%81%93%E5%9C%A8%E7%BA%BF/%E7%8E%8B%E9%81%93%E5%9C%A8%E7%BA%BF_files/report42f400.js#L291-L307) |
| `/mp/advertisement_report` 的 `report_type=1` | 对带有广告与跟踪标识的主曝光请求，在本机返回 `{"ret":0}`。公开页面把这个值视为上报成功，可避免它将同一次曝光重新入队。[曝光回调](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/index42f400.js#L1484-L1526) |

主点击上报（`report_type=2`）、广告落地页、投诉和「阅读原文」（`report_type=3`）继续按原流程处理。已有文章广告列表过滤继续处理已知广告字段。同份页面脚本还会通过原生桥接接口 `JSAPI.invoke("adDataReport")` 另行报告曝光。该调用未给出原生客户端的网络目的地，其覆盖情况和当前版本的实际命中均待验证。[原生桥接调用](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/index42f400.js#L1485-L1495) · [广告点击流程](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/index42f400.js#L1638-L1689) · [阅读原文流程](https://github.com/zhangdaiscott/jeewx/blob/dc6755e3d3793e4eb15ad99307a850881f0ea2ea/jeewx/src/main/webapp/plug-in/weixin/core/wx-article/appmsg1ef0d1.js#L25-L42)

**QQ 空间及腾讯广告 SDK。** 轻量版和懒人版按完整域名拦截 `rpt.gdt.qq.com` 的广告曝光报告和 `sdkreport.e.qq.com` 的广告 SDK 上报。QQ 空间的公开抓包记录识别出了曝光路径 `/creative_view`，另一份移动端记录还列出 SDK 的 `/link_event`。其他 App 若请求相同主机，也会命中这两条规则。QQ 当前客户端的实际命中仍待验证。[QQ 空间抓包规则](https://github.com/Aioneas/Surge/blob/1e69025a373d31153a46f8e48facf898eb27ac14/Module/qqzone.adblock.aioneas.sgmodule#L9-L22) · [曝光与 SDK 上报路径](https://github.com/Aioneas/Surge/blob/1e69025a373d31153a46f8e48facf898eb27ac14/Module/qqzone.adblock.aioneas.sgmodule#L49-L54) · [另一份移动端记录](https://github.com/xudazhu1/QuantumultX-/blob/e01472c5954b1eeb7291a68a84ba310b1eb8e582/qmkg.conf#L5-L6)

同样按完整域名拦截 `t.gdt.qq.com`。腾讯发布的 iOS 转化 SDK 使用该主机的 `/conv/sdk/spa/conv`，应用通过这条路径从设备上报广告转化。广告主服务器之间的归因回传不经过设备上的 Loon，仍可发生。[腾讯 iOS SDK 接入说明](https://qzonestyle.gtimg.cn/open_proj/gdt_gw/cms/uploads/ios-sdk-v1.4.pdf) · [官方 SDK 下载](https://imgcache.qq.com/qzone/biz/gdt/dev/sdk/ios/release/GDT_iOS_Track_SDK.zip) · [腾讯转化回传说明](https://qzonestyle.gtimg.cn/open_proj/gdt_gw/cms/uploads/conversion-api2-1108-.pdf)

上述三个主机的所有路径均受域名规则约束，包括使用 `?ADTAG=` 的请求。EasyList China 为 `qq.com` 网站列有这项通用放行。插件保留聊天、推送、登录和支付的共用主机，以及有具体路径放行记录的 `c.gdt.qq.com`、`v.gdt.qq.com`。广告主配置的第三方点击监测仍可能生效。[网页放行规则](https://github.com/easylist/easylistchina/blob/560a345168f36ca2bfbbf3280b0037451d6e3c80/easylistchina.txt#L15813-L15820) · [点击与统计路径的例外](https://github.com/xinggsf/Adblock-Plus-Rule/blob/65eb7d27b0716e6c92c9fddb8bc316aadc048e75/rule.txt#L264-L265) · [腾讯关于点击监测的说明](https://tencentads.com/Faqlist/Detail/397)

## 短视频和购物广告监测

| 场景 | 拦截范围 | 正常功能与证据边界 |
| --- | --- | --- |
| 穿山甲广告 SDK | 轻量版和懒人版均拦截 `log-api.pangolin-sdk-toutiao.com`、`log-api.pangolin-sdk-toutiao-b.com` 两个日志主机，无需证书。 | 使用穿山甲的 App 访问这两个主机时生效。抖音主 App 的推荐、直播和视频播放走各自接口，当前版本使用哪些原生广告监测接口仍待实机确认。[穿山甲日志主机清单](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L549-L550) |
| 淘宝手机网页版首页 | 懒人版针对轮播广告展示时发往 `ifs.tanx.com/display_ifs` 的指定 JSONP GET，在本机返回 HTTP 404。 | 官网脚本的两条轮播样例分开提供曝光地址和点击目标。曝光回调函数为空，脚本会在发起请求约 60 秒后清理未完成的回调。点按后使用的 `click.mz.simba.taobao.com/necpm`、商品详情、领券和下单均继续转发。淘宝原生 App 的同类曝光覆盖仍待确认。[淘宝首页脚本 3.3.45](https://g.alicdn.com/dinamic/h5-tb-home/3.3.45/index.min.js) |
| 京东广告曝光像素 | 懒人版匹配 `im-x.jd.com/dsp/np` 上依次含 `log` 和 `v=404` 的 GET，在本机返回 1×1 GIF。 | 公开商品搜索样例中的 3 个曝光地址全部命中。与它们成对出现的 3 个 `ccc-x.jd.com/dsp/nc` 点击地址均放行。京东商品、领券和结算请求仍走原路径。[曝光及点击样例](https://github.com/justoneapi-official/justoneapi-python/blob/fe5fb527f8b1b791635957d24280290155601a4c/docs/api-examples/getApiJdSearchItemListV2.json#L2662-L2663) · [网页请求记录，第 125 页](https://internet.hactcm.edu.cn/fileservice/network/file/2024/2/26/133534299256773962.pdf#page=125) |
| 拼多多广告联盟 | 懒人版仅在 GET 访问 `t-dsp.pinduoduo.com/dspcb/i/mrk_union` 且浏览器随请求发送 `Sec-Fetch-Dest: image` 时，在本机返回 1×1 GIF。 | 路径来自快递 100 适配。页面跳转、普通 fetch 和未携带图片标记的原生请求均放行。拼多多主 App 是否通过网页图片调用这个回调仍待确认，商品视频、订单和支付有独立的放行用例。[快递 100 适配](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partK/KuaiDi100.lpx#L154-L158) · [AdGuard 维护者跟帖](https://github.com/AdguardTeam/AdguardFilters/issues/225770#issuecomment-4045419446) |

三条购物回调规则均在发出请求前匹配，其他方法及相邻业务路径继续转发。使用懒人版并启用 HTTPS 解密后，这三个具名主机的其他流量也可能在设备上解密。本次已离线检查公开样例和合成请求。两台设备上当前版本的广告命中、播放体验、下单流程和网速尚未实测。

## 抖音主 App

这两条规则针对中国版抖音主 App 的推荐流和候选开屏路径。2026-11-21 查到的中国区 App Store 版本为 **41.2.0**。上游分析的是 iOS **30.3.0** 的安装包，测试使用合成响应；更早的字段实现只标注支持到 16.2.0。目前缺少 41.2.0 的 iPhone 或 iPad 广告响应和实机命中记录，实际使用的主机、路径和编码可能已经变化。抖音极速版及国际版 TikTok 另用各自客户端。[中国区 App Store](https://apps.apple.com/cn/app/id1142110895) · [30.3.0 静态证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L53) · [旧版适配说明](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Module/douyin.sgmodule#L1-L15)

- **主机范围**仅为 `api3-core-c.amemv.com`、`api3-normal-c.amemv.com`、`api.amemv.com`、`aweme.snssdk.com`。这些是共享 API 主机。开启解密后，发往这些主机的其他 HTTPS 请求也可能在本机经过 TLS 解密；插件只在指定路径执行复写。
- **推荐信息流**仅匹配 `/aweme/v1/feed` 和 `/aweme/v2/feed`。HTTP 200 的 JSON 须包含数值 `status_code=0` 和顶层 `aweme_list` 数组。仅当同页还含可识别的非广告作品或直播时，才过滤广告。作品取 `aweme_id`，直播取 `room_id`、`live_room.id` 或 `live_room.id_str`，这些标识须为正整数字样。过滤时只移除直接条目中 `is_ads` 为布尔 `true` 或数值 `1` 的对象。纯广告页、广告以外只有占位项的页面，以及找不到可识别作品或直播的页面均原样保留，避免翻页后只剩空白。带货和本地生活标记本身不会触发删除。其余条目的顺序、分页游标和预取字段保留。没有上述广告标记时直接返回，无需重新构造数组。[历史广告标记](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Script/douyin.js#L27-L43)
- **定向请求与编码**。查询参数名为 `aweme_id` 或 `aweme_ids` 的定向请求跳过处理。参数名含百分号编码时也跳过，避免改动指定作品。只有参数值含编码时，普通推荐仍按上述条件过滤。分享及其他视频路径、带明确失败标记的响应、Protobuf 等二进制响应和结构未知的 JSON 均保留。[上游数据格式边界](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L47-L65)
- **候选开屏接口**共有五个完整路径，分别为`/api/ad/v1/splash/stock`、`/api/ad/v16/splash/preload`、`/api/ad/splash/stock/realtime/v14`、`/api/ad/splash/stock/realtime/v15`、`/api/ad/splash/aweme/v15`。路径出自旧安装包；与前述四个主机的组合是基于静态配置的预防性匹配，缺少各组合的运行时捕获。拒绝请求后仍可能有本地倒计时、缓存画面或重试等待。[候选路径与证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/DouyinAdClean.snippet#L9-L17)

## 美团

美团部分包含 4 条原生复写，涉及 3 个完整主机名。美团的独立广告主机继续由域名规则拦截。[域名依据](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan.lpx#L12-L22)

| 场景 | 规则匹配与处理 | 验证边界 |
| --- | --- | --- |
| 美团主 App 开屏 | `mop.meituan.com/api/entryModule/startupPicture`。在匹配的 JSON 中，只清空 `resource` 或 `resourcesMap` 下名为 `startupPicArea` 的数组，兼容相应对象位于顶层或 `data` 中的结构。 | 上游注明适配 12.67.403。当前 iPad 客户端尚无实机命中记录。首页其他弹窗和分发路径可能继续显示。[上游版本](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L1-L3) · [请求路径](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L60-L63) · [结构](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L97-L109) |
| 美团外卖 App 开屏 | `wmapi.meituan.com/api/v7/loadInfo` 的已识别 JSON 中，只清空 `data.startpicture.ad` 广告数组。另用一条规则处理同主机 `/api/v7/openscreen`、`/api/v7/startpicture` 两个专用路径。 | `loadInfo` 的其他启动配置和 `mk` 字段保留。外卖首页推荐、商户菜单、配送费和订单各有自己的业务接口。外卖 App 的客户端版本与主 App 分开计算。[开屏字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [三个外卖路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) |
| 美团餐饮微信小程序 | `rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement` 的成功响应中，若报错、参数错误、冲突或未找到标志为真，则保留原响应。其余符合条件的响应只移除 `data.adSiteList` 内 `adSiteId` 符合 `adunit-…` 格式的条目，后缀限非空的英文字母、数字、下划线或连字符。 | 核查时匿名访问返回 HTTP 200、`code=200`、`success=true`，其中一个广告位经规则处理后变为零个，其他字段一致。这项结果来自公开接口响应。餐饮小程序的结账、企业餐和优惠权益不能用这条结果推断。[公开接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement) · [路径来源](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L19-L27) |
| 共享图片主机 | p0.meituan.net、p1.meituan.net、img.meituan.net 保留原始 HTTPS 连接。 | 三个主机也提供正常酒店图或商品图。原来在这些主机上过滤的部分广告素材可能再次显示。[点评酒店图片文档](https://h5.dianping.com/app/bep-docs/sky-doc/hotelopenapi/hotel_open_api_interface.html) · [美团订单商品图文档](https://h5.dianping.com/app/bep-docs/sky-doc/ordercenter/orderdetail_api.html) |

上述 6 个主机承载的其他 HTTPS 请求也可能在本机经过 TLS 解密。网络耗时、缓存条件和 App 实现都会影响实际体验。菜单图片、结算页或优惠券出现异常时，可停用懒人版，在同一网络重复打开相同页面，比对两次结果。[Loon 解密范围](https://nsloon.app/docs/MitM/)

## 购物和生活

| App | 已实现的规则 | 适用条件与保留内容 |
| --- | --- | --- |
| 京东 | 京媒广告请求、另一竞价主机的 `/adx/` 路径。能识别操作名时，清空开屏图和次数，剔除首页两种悬浮推广楼层 | 要求 URL 中只有一个明确的 `functionId=start` 或 `functionId=welcomeHome`。同一请求出现无值或重复的操作名、或含百分号编码的参数名时跳过。普通参数值仍可编码。新版可能把操作名及正文编码，此时这两条复写会跳过。商品图片 CDN、比价、优惠券、购物车和订单均未列为拦截目标。[京媒 SDK](https://help-sdk-doc.jd.com/ansdkDoc/faq/faq.html) · [首页字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [竞价接口](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/jd_splash_ad_block.plugin#L19-L25) · [新版样本和限制](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/tests/jd-test.js#L26-L50) |
| 淘宝 | 手机网页版首页的指定轮播曝光回调 | 淘宝与菜鸟共用的 MTOP 网关保留原始 HTTPS 连接。淘宝 App 这处开屏广告可能再次显示。[消息排查](#淘宝消息排查) |
| 菜鸟 | 淘宝与菜鸟共用的 MTOP 网关保留原始 HTTPS 连接 | 原先针对该网关的菜鸟广告过滤已撤下。[菜鸟 App 网关记录](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CHANGELOG.md#L24-L27) |
| 拼多多 | 开屏配置、首页及刷新接口中标为 `ad_module` 的模块，以及已知混合搜索页的付费商品卡。 | 首页只按明确的模块名过滤。个人中心的取货通知与优惠横幅整块保留。订单、支付、优惠券、聊天和普通商品推荐有保留用例。本次验证用的是离线样本。[开屏配置](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partP/Pinduoduo.lpx#L11-L14) · [首页字段](https://github.com/ishowshu/qx/blob/3ad7bec45ec25cd41edfbae70db3869106e01890/script/pdd.js#L30-L46) · [刷新路径](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/Pinduoduo.snippet#L24) |
| 快递 100 等接入拼多多广告联盟的 App | 拦截 `video-dsp.pddpic.com` 的推广视频素材。公开路径记录来自快递 100，规则按完整域名生效。 | 运单接口、商品图片和普通视频域名不在本条规则中。[素材路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partK/KuaiDi100.lpx#L154-L158) · [独立域名记录](https://github.com/vokins/ad/blob/5f177915e12fbaed055dd2ef79f56b97f689ac58/ad.lsr#L341) |
| 闲鱼 | 共用的 MTOP 业务网关保留原始 HTTPS 连接 | 闲鱼技术团队记录了用 MTOP 拉取消息的机制。同步和异步开屏广告可能再次显示。[闲鱼消息团队技术说明](https://juejin.cn/post/7005836853001748517) |
| 大众点评 | 按精确主机拦截 ad.api.dianping.com 的独立广告请求。 | 点评 App 网关与桌面网页保留原始 HTTPS 连接，App 开屏与网页城市横幅可能再次显示。[点评网络团队对广告域名的说明](https://tech.meituan.com/2017/03/17/shark-sdk.html) |
| 高德地图、铁路 12306 | 高德的两条启动广告接口，铁路 12306 的独立广告主机 | 路线、导航、查票和购票接口不在名单中。App 自带的开屏倒计时可能继续显示。[高德地图](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partG/AutoNavi.lpx#L27-L36) · [铁路 12306](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/part1/12306.lpx#L14-L22) |

**拼多多搜索**　规则只处理已知 `api.pinduoduo.com/search` 的成功 JSON。混合结果中，卡片须同时具备商品名称、匹配的商品 ID、广告创意 ID、商家 ID 及数值大于零的广告竞价（`ocpcBid`）才会移除。同件商品的自然结果、优惠信息和翻页游标都会保留。若整页都是推广，规则保留原页，避免产生无法继续翻页的空列表。[公开搜索接口与字段](https://github.com/zheng515253/spiderDemo/blob/da58b9332336118e185517fc741d9f72fc1e9452/pddSpider/spiders/pdd_keyword_goods_v8.py#L92-L111) · [搜索路径记录](https://github.com/Reukix/ukix/blob/44daad38c7d9b24379cb969f2a1a89ca49ec3297/Script/Pinduoduo.sgmodule#L27)

将 99 张公开历史商品卡放入模拟分页响应，实际规则移除了 11 张推广卡，其余 88 张内容及顺序一致。核查时，搜索接口向匿名请求返回 HTTP 403，当前 iOS 版本是否仍走同一接口有待实测。[历史商品样本](https://github.com/onetwo1/pinduoduo/blob/021ed7772373ef382ef7f96f006cc92b4201035a/pin_duoduo/pin_duoduo/data/data.json#L5-L7) · [回归用例](tests/test_pdd_updates.py)

### 淘宝消息排查

在 Loon 刷新原订阅后，请用同一网络分别测试淘宝消息页能否收到新消息，以及锁屏时有无通知。若问题仍在，可在同一台设备上切换本插件，对比两次收到的情况。锁屏通知还可检查 iOS 里淘宝的通知权限。排查时记录 Loon 命中的规则和主机名即可，勿分享聊天内容或带令牌的完整请求 URL。[淘宝开放平台消息说明](https://developer.alibaba.com/docs/doc.htm?articleId=103423&docType=1&treeId=55) · [Apple 推送网络要求](https://support.apple.com/zh-cn/102266)

### 大众点评和山姆卡顿排查

大众点评技术团队将商户图和笔记头图列为影响移动网页首屏渲染的资源。新版收窄点评网关、网页和美团共用图床的解密范围，已用公开的酒店与商品图片核对三个图床。实机加载耗时需用同一网络、同一店铺页面对照。[点评首屏研究](https://tech.meituan.com/2026/03/13/Qwik-practice-in-dianping.html)

山姆已核对官网、会员协议、购物网关和网页资源主机的规则匹配。旧的第三方规则曾被报告影响山姆购物车和订单。若山姆仍卡，在同一网络下只切换本插件，分别打开同一商品页或购物车，并在 Loon 请求记录中查慢请求的主机、策略及实际命中的插件。分享日志时仅保留主机和规则名称即可。[山姆会员协议](https://m-sams.walmartmobile.cn/common/terms-of-agreement?agreementType=3) · [第三方规则历史反馈](https://github.com/blackmatrix7/ios_rule_script/issues/881) · [第三方规则现有匹配](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/rewrite/Loon/AllInOne/AllInOne.plugin#L214)

## 国产 App 的独立广告主机

轻量版和懒人版都能按以下完整主机名拦截广告请求，无需证书和 HTTPS 解密。客户端从其他主机投放、从缓存读取的广告，以及已经录入节目里的口播，仍可能出现。

| App | 拦截位置与依据 |
| --- | --- |
| 墨迹天气 | `ad.api.moji.com`、`adlaunch.moji.com` 的广告与开屏请求。天气服务 `wwwapi.moji.com` 可继续访问。[墨迹天气规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/MojiWeather.lpx#L17-L19) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L64480-L64481) |
| 百词斩 | `advertise.baicizhan.com` 和 `advertise.baicizhan.org` 的广告请求。阅读和登录使用各自的主机。[百词斩规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partB/baicizhan.lpx#L13-L14) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L15197-L15198) |
| 网易有道词典 | `dsp-impr2.youdao.com` 的广告加载和 `impservice.dictapp.youdao.com` 的广告请求。两个主机按完整域名拦截，查词与口语服务的主机可继续访问。[广告接口](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partW/NetEaseYoudaoDictionary.lpx#L35-L37) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L107618-L107624) |
| 讯飞输入法 | 拦截访问广告主机 `bj.imp.voiceads.cn` 的请求。匹配限于这个主机，输入内容和语音服务不参与规则判断。[讯飞输入法规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partX/iFlytekInputMethod.lpx#L13-L16) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L100325) |
| 虎扑 | `adx.hupu.com` 的广告交易请求。赛事、社区和普通图片使用的其他主机可继续访问。[虎扑规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partH/Hupu.lpx#L13-L14) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L48011) |
| 澎湃新闻 | `adpai.thepaper.cn` 的投放请求。普通新闻图片、视频与音频位于其他主机。[澎湃新闻规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partP/ThePaperNews.lpx#L13-L15) · [EasyList China 广告分类](https://github.com/easylist/easylistchina/blob/560a345168f36ca2bfbbf3280b0037451d6e3c80/easylistchina.txt#L6792) |
| 虎嗅 | `api-ad-product.huxiu.com` 提供广告列表查询，路径包括 `/Api/Product/SDK/Advert/Query/queryAdvertListInfo`。[广告查询接口](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partH/Huxiu.lpx#L12-L14) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L48070) |
| 凤凰新闻 | `api.newad.ifeng.com` 的广告请求。[凤凰新媒体规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partF/PhoenixNewMedia.lpx#L27) · [域名交叉核对](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/anti-ad-domains.txt#L49094) |
| 七猫免费小说 | `cdn-new-ad.wtzw.com` 的广告素材。章节正文和奖励领取接口各有自己的路径，奖励视频若使用该素材主机也可能无法加载。[七猫规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partQ/QiMaoNovel.lpx#L13-L15) · [广告素材分类](https://github.com/vokins/ad/blob/5f177915e12fbaed055dd2ef79f56b97f689ac58/ad.lsr#L291-L294) |
| 喜马拉雅 | `adse.ximalaya.com`、`adse.wsa.ximalaya.com` 的广告请求。移动端公开记录将这两台主机与开屏和小组件联系起来。[广告域名分类](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/ximalaya#L4-L7) · [移动端报告](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/issues/109) |
| 酷狗音乐 | `ads.service.kugou.com` 及备用广告主机 `adserviceretry.kugou.com`。[广告域名分类](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/kugou#L18-L21) · [酷狗规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partK/KuGouMusic.lpx#L13-L15) |
| 蜻蜓 FM | `ad.qingting.fm` 的广告投放请求和 `ad-cdn.qingting.fm` 的广告素材。[蜻蜓 FM 规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partQ/QingTingFM.lpx#L12-L15) · [精确域名清单](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L31-L57) |

## 更多常用 App 的广告位

下表前六项在轻量版和懒人版中均可使用，无需安装证书。它们按完整域名生效，其他 App 若请求同一广告主机也会被拦截。

| App | 拦截位置 | 来源 |
| --- | --- | --- |
| 米家 | 小米广告 SDK 的配置主机 `sdkconfig.ad.xiaomi.com`。其他渠道提供的推广卡仍可能出现。 | [米家规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Mijia.lpx#L13-L18) · [广告域名表](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L771) |
| 同花顺系 App | 拦截 `adm.10jqka.com.cn` 的广告请求。公开记录来自同花顺 iFinD，其他版本须实际访问同一主机才会命中。 | [iFinD 广告主机](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partT/iFinD.lpx#L13-L19) |
| LINE | 广告素材主机 `ad.line-scdn.net`。 | [LINE 规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partL/Line.lpx#L30-L34) · [AdGuard 移动广告清单](https://github.com/AdguardTeam/AdguardFilters/blob/1256f5db2a6fe797fc93960ab904e1930f7aeef5/MobileFilter/sections/adservers.txt#L348) |
| 百度地图 | 百度信息流的广告投放与配置主机 `afd.baidu.com`、`afdconf.baidu.com`。 | [地图广告规则](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partB/BaiduMaps.lpx#L15-L19) · [百度域名分类](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/baidu#L91-L92) |
| 下厨房 | 百度联盟的脚本与广告位主机 `baidu-union-js.xiachufang.com`、`baidu-union-pos.xiachufang.com`。 | [下厨房广告主机](https://github.com/zirawell/R-Store/blob/a4f3b10d6038d77ae3e1ff68bd19a49071ebabd3/Rule/QuanX/Adblock/App/X/%E4%B8%8B%E5%8E%A8%E6%88%BF/snippet/xiachufang.snippet#L12-L17) |
| 美图秀秀 | 广告服务主机 `adui.tg.meitu.com`。 | [美图秀秀广告主机](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partM/MeituXiuxiu.lpx#L16-L19) |

以下广告位由懒人版的原生复写处理。开启 HTTPS 解密后，同一主机的其他流量也可能在本机被解密。表中列出复写实际匹配的路径或字段。

| App | 拦截位置与范围 | 来源 |
| --- | --- | --- |
| 百度贴吧 | 看图模式的批量广告接口 `tiebac.baidu.com/tiebaads/commonbatch`。查询中须有一个明确的 `adcmd`。只在成功 JSON 的 `res.ad` 是非空对象数组时清空它。帖子、图片列表和 JSONP 回调保持原样。 | [上游路径](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/module/tieba.sgmodule#L10-L15) · [响应字段](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/tieba-json.js#L17-L35) |
| 得物 | `app.dewu.com/api/v1/app/advertisement` 开屏广告配置。 | [得物开屏](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partD/DeWu.lpx#L13-L15) |
| 猫眼 | `p0.pipi.cn` 的 `/adAdmin/` 和 `/mediaplus/maoyantong_ads_fe/` 两个广告目录。仅匹配 GIF 或带指定质量、尺寸参数的 JPG、PNG。 | [广告图片目录](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partM/MaoYan.lpx#L13-L15) · [文件格式与参数](https://github.com/zirawell/R-Store/blob/a4f3b10d6038d77ae3e1ff68bd19a49071ebabd3/Rule/QuanX/Adblock/App/M/%E7%8C%AB%E7%9C%BC/snippet/pipi.snippet#L13-L15) |
| 转转 | `app.zhuanzhuan.com/zz/v2/zzlogic/getOpenScreen` 开屏配置。 | [转转开屏](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partZ/ZhuanZhuan.lpx#L15-L21) |
| BOSS 直聘 | `api-ios.zhipin.com/api/zpCommon/user/startupAd` 启动广告。 | [iOS 启动广告接口](https://github.com/zirawell/R-Store/blob/a4f3b10d6038d77ae3e1ff68bd19a49071ebabd3/Rule/QuanX/Adblock/App/B/Boss%E7%9B%B4%E8%81%98/snippet/boss.snippet#L13-L15) |
| 去哪儿 | `homefront.qunar.com/front/splash/ad` 独立开屏广告请求。 | [去哪儿开屏](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partQ/Qunar.lpx#L14-L16) |
| 飞常准 | `app.variflight.com` 上的 `/ad/` 和 `/v1/advert/` 两个广告目录，只匹配普通路径段。 | [飞常准广告目录](https://github.com/fmz200/wool_scripts/blob/58f6cce6dbd5c5fe50c2998938f9c2ba631a7c18/Loon/plugin/split/partF/VariFlight.lpx#L19-L22) |
| 北京银行信用卡「掌上京彩」 | 静态主机 `cdn-xyk-app.bankofbeijing.com.cn` 的 `/cdn/resource/image/advertise/` 中，以 JPG、JPEG、PNG、GIF 或 WebP 为扩展名的图片。 | [广告图片目录](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partB/ZhangShangJingCai.lpx#L12-L14) |
| 广发信用卡「发现精彩」 | 静态主机 `static.95508.com` 的 `/mmg/ciop/sysabbr/cmep/images/` 下，限 `apppopupads/`、`popupads/` 两个目录和上述图片格式。 | [弹窗广告目录](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partF/FaXianJingCai.lpx#L14-L15) |

公开规则与离线样本可用于核对匹配范围。这些广告位在当前 iPhone、iPad 版本上的实际命中和启动耗时还待验证。广告素材如已缓存，首次重新打开 App 时仍可能显示。

## 内容和影音

**YouTube** 的 Safari 网页助手可单独安装，支持首页和搜索结果里的部分独立广告位，以及普通播放页上已经可点击的「跳过广告」按钮。插件中的 Google 广告域名规则不能保证过滤原生 YouTube App 的片头和中插。独立助手无需开启 HTTPS 解密。[范围与安装](youtube/README.md)

| App | 已实现的规则 | 适用条件与依据 |
| --- | --- | --- |
| 小红书、知乎 | 小红书首页去掉带非空 `ads_info` 对象的广告卡，另拦三台广告素材主机。知乎首页按 `type=feed_advert` 过滤 | 小红书保留仅有商品关联、直播标记的普通条目，知乎保留未知类型。作者自行植入的推广通常没有这类标记。[小红书](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xiaohongshu_splash_ad_block.plugin#L58-L65) · [知乎](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) |
| 哔哩哔哩 App 开屏 | 在 `/x/v2/splash/list` 的成功 JSON 中，素材同时满足 `is_ad=true`、`cm_mark=1` 和有效数值 ID 时才移除。`show`、`keep_ids` 只清理同一响应中仅属于已删广告的数值引用。 | 固定资料中的一条商业素材被识别。独立的品牌图、活动和曝光上报接口继续使用原响应。实际客户端是否使用该路径，仍取决于版本与投放。[开屏响应样本](https://github.com/realysy/bili-apis/blob/3802052be89effc3bbd27574037942310a23672d/docs/APP_widget/splash.md#L321-L351) · [移动端请求观测](https://github.com/UserC23/bilibili-ads-loon/blob/38ad51c6bef2be64625b7a86e9bf8aac44a4119a/docs/analysis.md#L36-L46) |
| 微信、哔哩哔哩 | 公众号文章广告列表、B 站 App 首页的推广卡和混排横幅中的广告子项。 | 微信文章保留阅读互动。B 站只按卡片类型和去向移除推广，普通视频或直播卡可以带有 `ad_info`。网页首页的推荐使用原始响应，推广卡可能显示。[内嵌广告说明](README.md#内嵌广告) |
| 微博主 App | 关注流的 `statuses` 以及首页、推荐流的 `items` 中，只移除带数值 `is_ad=1` 或精确标签 `mblogtypename="广告"` 的微博。另有原有开屏和素材主机规则。 | 普通微博、文字里出现“广告”的正文和未标记推广继续显示。保留正常微博的顺序及分页字段。[广告标记](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L140-L155) · [关注流](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L438-L452) · [首页和推荐](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L96-L102) |
| 微博轻享版 | 在 `api.weibo.cn/2/ad/weibointl` 的成功 JSON 中，仅清空 `data` 广告数组。 | 只匹配这条路径，覆盖取决于当前版本是否使用它。[轻享版专用接口](https://github.com/gj0134/Loon-Plugins/blob/5c835d0db14a4808c19cd010641be1235b6b3d73/plugins/Weibo-Intl-AdBlock.plugin#L7-L16) |
| 酷安 | 在 `api.coolapk.com/v6/main/dataList`、`/v6/main/indexV8` 成功返回的 `data` 数组中，只移除 `entityTemplate="sponsorCard"` 的赞助卡。 | 普通动态、带商品的内容及带“红包”等字样的卡片可正常保留。页面仍可能展示未带该标记的推广。[赞助卡字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/coolapk.js#L28-L44) |
| 网易云音乐、QQ 音乐 | 网易云开屏图片及视频广告素材，QQ 音乐广告投送及素材 | 播放与普通封面 CDN 不在域名拦截中。[网易云](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/NeteaseCloudMusic_ads_v2.lpx#L8-L12) · [QQ 音乐](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/qqmusic_splash_ad_block.plugin#L14-L20) |
| 腾讯视频、优酷 | 腾讯广点通广告素材主机、优酷广告交易主机。 | 这些域名覆盖部分外部广告请求。与正片合流的广告和口播仍可能播放。[腾讯视频](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/tencentvideo_splash_ad_block.plugin#L13-L19) · [优酷](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/youku_splash_ad_block.plugin#L18-L24) |
| 爱奇艺 | 外部 Tanx 广告主机；首页与搜索结果中有明确广告标记的卡片；官网频道页已识别的焦点图和内容卡视频广告位。 | 卡片和广告位使用本机响应过滤，需对 `cards.iqiyi.com` 和 `t7z.cupid.iqiyi.com` 开启 HTTPS 解密。当前证据限于已知接口和两个展示位，未验证能跳过播放器的片头、片中广告或视频内口播。[卡片字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/cnftp.js#L146-L156) · [搜索字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/cnftp.js#L223-L241) · [接口路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partA/iQIYI.lpx) · [爱奇艺官网频道资源](https://www.iqiyi.com/static/js/channel_afbe97b7.56f893f6.js) |

懒人版还涵盖百度、字节穿山甲、快手、Google 和 WPS 等已知广告主机。域名规则、原生复写和完整解密主机名可查看[插件原文](iPad-AdSuite.lpx)。

### 哔哩哔哩播放排查

视频详情、播放地址和网页首页推荐共用 `api.bilibili.com`。Loon 按主机名决定是否解密 HTTPS。只复写网页推荐这一条路径，也会让该主机上的播放请求进入解密。懒人版和内嵌版已移除这个主机，App 首页与开屏的两条规则仍在 `app.bilibili.com` 上运行。公开的 iOS 客户端抓包在同一次会话里记录了 3 次播放地址请求和 1 次视频详情请求。[Loon 解密范围](https://nsloon.app/docs/MitM/) · [移动端抓包记录](https://github.com/UserC23/bilibili-ads-loon/blob/38ad51c6bef2be64625b7a86e9bf8aac44a4119a/docs/analysis.md#L241-L253)

另一次匿名测试中，番剧 `ep267851` 的播放接口成功返回地址，但分配的音频和视频主节点均在 TLS 握手时超时，同一响应给出的四个备用地址都返回了媒体数据。另一条普通视频使用同一 CDN 域下的不同节点时可以读取。这种情况下，封禁整个 CDN 也会挡住可用节点。

若某条视频仍打不开，可在同一网络下用 App 和 Safari 打开同一 BV 号，并在 Loon「请求记录」里核对失败时间、主机和命中的规则来源。其他插件或主配置仍可能把 `api.bilibili.com` 列入解密。排查时只需比较相关配置，保留现有代理策略，无需把全部 B 站域名改为直连。桌面浏览器已验证一条免费视频能开始播放，其余公开样本核对到媒体数据开头。用户设备上的故障仍待实测。[本次验证](SECURITY-AUDIT.md#2026-11-23--哔哩哔哩播放兼容性)

## 已完成的验证

回归测试使用离线样例核对插件中的实际 URL 正则及 jq 过滤器。购物样例包含错误响应、未知结构、相似操作名、正常商品和优惠券。测试还核对原有规则、正常业务路径及主机名单。真实广告命中率、实际吞吐量和 HTTPS 解密耗时需要在启用后的 iPhone 或 iPad 上验证。在仓库根目录运行 `python -m unittest discover -s tests` 可运行整套离线回归测试。[抖音专项](tests/test_mobile.py) · [微博与酷安](tests/test_social.py) · [美团专项](tests/test_meituan.py) · [购物与常见 App 测试](tests/test_suite.py) · [原内嵌规则测试](tests/test_inline.py)

## 在 iPad 上核对单条规则

- **域名拦截**无需 HTTPS 解密。用 Safari 打开下方的 Google 广告脚本，再到 Loon「仪表 → 请求记录」搜索 `pagead2.googlesyndication.com`。打开刚才的记录，核对策略为 `REJECT`、规则来源为正在验证的插件。Safari 的加载错误本身无法说明由谁拦截。[打开 Google 广告脚本](https://pagead2.googlesyndication.com/tag/js/gpt.js?loon_check=1) · [Google 官方脚本地址说明](https://developers.google.com/publisher-tag/guides/general-best-practices) · [Loon 请求详情的来源字段](https://t.me/LoonNews/706)
- **美团响应复写**适用于已启用懒人版并已为该主机配置 HTTPS 解密的设备。用 Safari 打开下方的公开接口，在 Loon 请求记录中搜索 `queryWechatAdvertisement`，点开同一时间的请求，查看命中的响应复写及其来源「常用 App 去广告（懒人版）」。服务端也可能直接返回空的 `adSiteList`。如要核对条目变化，可仅切换本插件，在同一网络刷新接口，比对停用时出现的 `adunit-…` 广告位和启用后的结果，再恢复原状态。两次都为空则无法通过响应内容判定。[打开美团餐饮微信广告位接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement)
