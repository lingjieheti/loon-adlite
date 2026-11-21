# 常用 App 去广告的覆盖范围

iPhone 和 iPad 共用[懒人版订阅](README.md#安装)。截至 2026-11-21，插件含 45 条精确域名规则和 28 条原生复写。域名拦截无需证书。部分开屏和信息流广告需要 HTTPS 解密，插件为此列出了 27 个完整主机名。同一款 App 可能同时使用广告联盟、自己的内容接口及服务端视频插播。以下列出已实现的广告位置，规则数量不能换算为拦截率。

## 网页广告

- **网页竞价广告**。Loon 拦截 PubMatic、Criteo 和 TripleLift 的指定竞价主机。新增的 `tlx.3lift.com` 用于 Prebid 的浏览器竞价，AdAway 也收录了这个完整主机名。同一广告位可能向其他广告商询价。[PubMatic](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/pubmaticBidAdapter.js#L25) · [Criteo](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/criteoBidAdapter.js#L27) · [TripleLift](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/tripleliftBidAdapter.js#L10) · [AdAway](https://github.com/AdAway/adaway.github.io/blob/f39ba0a523564447dfa94e40327c1a14c02304dc/hosts.txt#L81)
- **百度联盟展示广告**。AMP 的百度广告组件从 `dup.baidustatic.com` 加载广告脚本，EasyList China 也将其列为广告主机，因此插件精确拦截该主机。另一个广告主机 `cpro.baidustatic.com` 有四个网站的指定脚本放行例外，因此留给能识别来源网页和路径的浏览器过滤器处理。[AMP 百度广告组件](https://github.com/ampproject/amphtml/blob/29d4f68e5a1017ed5d63e3086b219b4b25a41332/ads/vendors/baidu.js#L16-L35) · [EasyList China 主机规则](https://github.com/easylist/easylistchina/blob/7efab892b13dc99ed81f1995887a9c0f79510362/easylistchina.txt#L7928) · [网站例外](https://github.com/easylist/easylistchina/blob/7efab892b13dc99ed81f1995887a9c0f79510362/easylistchina.txt#L15828-L15829)
- **Pornhub 网页**。Loon 另拦 `a.adtng.com` 和 `ads.trafficjunky.net`。页面内嵌广告、同源投放及拼入正片的片段仍可能出现。这两条全局规则也会影响其他网站。EasyList 允许 `hanime.tv` 的部分嵌入框架访问 `adtng.com/get/`；若框架实际使用 `a.adtng.com`，Loon 的域名拦截仍会生效。尚未验证该站的实际播放影响。[域名清单](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/category-ads#L74-L81) · [TrafficJunky 广告位](https://www.trafficjunky.com/advertiser/ad-formats) · [EasyList 框架例外](https://github.com/easylist/easylist/blob/68a1b6472a6954f713eb62f3919ca7b8301f5ab4/easylist/easylist_allowlist.txt#L489)
- **Safari 页面清理**。可选助手通过站点专用 CSS 隐藏部分侧栏、移动播放页广告容器及明确标记的投放元素。它可以清掉部分广告占位，无法识别已经拼进视频的广告。该功能需用支持用户脚本的扩展单独安装。[网页助手](web/pornhub.user.js)

离线测试核对上述广告主机的精确匹配，并检查主域、共享 CDN、相似主机和正常视频路径。当前缺少这些广告位在 iPad 上的实机命中记录，也未测量启用前后的吞吐量。[域名回归测试](tests/test_suite.py)

**开源规则如何搭配**。2026-11-21 比对的 HaGeZi Multi LIGHT 快照含 91,706 个不同域名。项目更新前的 43 个广告主机中，21 个与该清单完全相同，另有 11 个落在它列出的父域之下。这个数字反映清单重叠程度。Loon 订阅只保留选定的完整主机；需要处理普通网页里的横幅和空位时，可以在 Safari 里选用 AdGuard 的基础和中文过滤器，让浏览器应用页面规则和网站例外。[对比用的插件版本](https://github.com/lingjieheti/loon-adlite/blob/ae273c03c32c98f7dafe938aed4e05fdcfd9045a/iPad-AdLite.lpx) · [HaGeZi 固定快照](https://github.com/hagezi/dns-blocklists/blob/6033fe872ee360ff34da5a9e826558030938fc7e/wildcard/light-onlydomains.txt) · [Safari 可选设置](web/README.md#普通网页仍有横幅或广告空位)

## 抖音主 App

这两条规则针对中国版抖音主 App 的推荐流和候选开屏路径。2026-11-21 查到的中国区 App Store 版本为 **41.2.0**。上游分析的是 iOS **30.3.0** 的安装包，测试使用合成响应；更早的字段实现只标注支持到 16.2.0。目前缺少 41.2.0 的 iPhone 或 iPad 广告响应和实机命中记录，实际使用的主机、路径和编码可能已经变化。抖音极速版及国际版 TikTok 另用各自客户端。[中国区 App Store](https://apps.apple.com/cn/app/id1142110895) · [30.3.0 静态证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L53) · [旧版适配说明](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Module/douyin.sgmodule#L1-L15)

- **主机范围**仅为 `api3-core-c.amemv.com`、`api3-normal-c.amemv.com`、`api.amemv.com`、`aweme.snssdk.com`。这些是共享 API 主机。开启解密后，发往这些主机的其他 HTTPS 请求也可能在本机经过 TLS 解密；插件只在指定路径执行复写。
- **推荐信息流**仅匹配 `/aweme/v1/feed` 和 `/aweme/v2/feed`。HTTP 200 的 JSON 须包含数值 `status_code=0` 和顶层 `aweme_list` 数组。仅当同页还含可识别的非广告作品或直播时，才过滤广告。作品取 `aweme_id`，直播取 `room_id`、`live_room.id` 或 `live_room.id_str`，这些标识须为正整数字样。过滤时只移除直接条目中 `is_ads` 为布尔 `true` 或数值 `1` 的对象。纯广告页、广告以外只有占位项的页面，以及找不到可识别作品或直播的页面均原样保留，避免翻页后只剩空白。带货和本地生活标记本身不会触发删除。其余条目的顺序、分页游标和预取字段保留。没有上述广告标记时直接返回，无需重新构造数组。[历史广告标记](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Script/douyin.js#L27-L43)
- **定向请求与编码**。查询参数名为 `aweme_id` 或 `aweme_ids` 的定向请求跳过处理。参数名含百分号编码时也跳过，避免改动指定作品。只有参数值含编码时，普通推荐仍按上述条件过滤。分享及其他视频路径、带明确失败标记的响应、Protobuf 等二进制响应和结构未知的 JSON 均保留。[上游数据格式边界](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L47-L65)
- **候选开屏接口**共有五个完整路径，分别为`/api/ad/v1/splash/stock`、`/api/ad/v16/splash/preload`、`/api/ad/splash/stock/realtime/v14`、`/api/ad/splash/stock/realtime/v15`、`/api/ad/splash/aweme/v15`。路径出自旧安装包；与前述四个主机的组合是基于静态配置的预防性匹配，缺少各组合的运行时捕获。拒绝请求后仍可能有本地倒计时、缓存画面或重试等待。[候选路径与证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/DouyinAdClean.snippet#L9-L17)

## 美团

美团部分包含 6 条原生复写，涉及 6 个完整主机名。美团的独立广告主机继续由域名规则拦截。[域名依据](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan.lpx#L12-L22)

| 场景 | 规则匹配与处理 | 验证边界 |
| --- | --- | --- |
| 美团主 App 开屏 | `mop.meituan.com/api/entryModule/startupPicture`。在匹配的 JSON 中，只清空 `resource` 或 `resourcesMap` 下名为 `startupPicArea` 的数组，兼容相应对象位于顶层或 `data` 中的结构。 | 上游注明适配 12.67.403。当前 iPad 客户端尚无实机命中记录。首页其他弹窗和分发路径可能继续显示。[上游版本](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L1-L3) · [请求路径](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L60-L63) · [结构](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L97-L109) |
| 美团外卖 App 开屏 | `wmapi.meituan.com/api/v7/loadInfo` 的已识别 JSON 中，只清空 `data.startpicture.ad` 广告数组。另用一条规则处理同主机 `/api/v7/openscreen`、`/api/v7/startpicture` 两个专用路径。 | `loadInfo` 的其他启动配置和 `mk` 字段保留。外卖首页推荐、商户菜单、配送费和订单各有自己的业务接口。外卖 App 的客户端版本与主 App 分开计算。[开屏字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [三个外卖路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) |
| 美团餐饮微信小程序 | `rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement` 的成功响应中，若报错、参数错误、冲突或未找到标志为真，则保留原响应。其余符合条件的响应只移除 `data.adSiteList` 内 `adSiteId` 符合 `adunit-…` 格式的条目，后缀限非空的英文字母、数字、下划线或连字符。 | 核查时匿名访问返回 HTTP 200、`code=200`、`success=true`，其中一个广告位经规则处理后变为零个，其他字段一致。这项结果来自公开接口响应。餐饮小程序的结账、企业餐和优惠权益不能用这条结果推断。[公开接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement) · [路径来源](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L19-L27) |
| 广告素材 | 一条规则匹配 `p0.meituan.net` 和 `p1.meituan.net` 的 `/adunion/`，另一条匹配 `img.meituan.net/bizad/bizad_brandCpt_数字.jpg`，以及该主机 `/adunion/` 目录内以 `.gif.webp` 或 `.jpg.webp` 结尾的素材。 | 同主机上其他目录的商户、菜品和评价图片不会命中这两条规则。素材请求被拦后，客户端仍可能留下占位或等待重试。[p0/p1 目录](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/MeituanAppAdMedia.snippet#L4-L7) · [品牌图文件名](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) · [img 素材后缀](https://github.com/zirawell/R-Store/blob/d0f4dd305bade7cc6a38e3445a768d72aaea0e5b/Rule/QuanX/Adblock/App/M/%E7%BE%8E%E5%9B%A2/rewrite/meituan.conf#L4) |

上述 6 个主机承载的其他 HTTPS 请求也可能在本机经过 TLS 解密。网络耗时、缓存条件和 App 实现都会影响实际体验。菜单图片、结算页或优惠券出现异常时，可停用懒人版，在同一网络重复打开相同页面，比对两次结果。[Loon 解密范围](https://nsloon.app/docs/MitM/)

## 购物和生活

| App | 已实现的规则 | 适用条件与保留内容 |
| --- | --- | --- |
| 京东 | 京媒广告请求、另一竞价主机的 `/adx/` 路径。能识别操作名时，清空开屏图和次数，剔除首页两种悬浮推广楼层 | 要求 URL 中只有一个明确的 `functionId=start` 或 `functionId=welcomeHome`。同一请求出现无值或重复的操作名、或含百分号编码的参数名时跳过。普通参数值仍可编码。新版可能把操作名及正文编码，此时这两条复写会跳过。商品图片 CDN、比价、优惠券、购物车和订单均未列为拦截目标。[京媒 SDK](https://help-sdk-doc.jd.com/ansdkDoc/faq/faq.html) · [首页字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [竞价接口](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/jd_splash_ad_block.plugin#L19-L25) · [新版样本和限制](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/tests/jd-test.js#L26-L50) |
| 淘宝 | 淘宝开屏配置的 `taobao-splash` 槽，仅移除含有效 HTTP、HTTPS 或协议相对素材地址的广告条目，保留只有跳转链接、空协议或无主机的条目 | 校验方法名、版本和 MTOP 成功状态。正常首页、红包、商品视频、详情和结算不在复写路径中。首页混排的商业推荐仍可能出现。[淘宝开屏字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/myBlockAds.js#L84-L121) |
| 菜鸟 | 淘宝网关中菜鸟专用广告投放接口的成功响应 | 仅在接口和响应形状吻合时清空广告数据。即使网关返回成功，业务层明确失败或返回非空 `errmsg` 时也保留原响应。[MTOP 网关与业务状态示例](https://developer.alibaba.com/support/hotProblemDetail.htm?id=346101&source=doc) 没有取得真实成功投放响应。[菜鸟维护者规则](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CainiaoAds.plugin#L49-L50) |
| 拼多多、闲鱼 | 拼多多的开屏配置路径，闲鱼的同步和异步开屏广告方法 | 只匹配指定路径或方法，不封购物网关。商品推荐、优惠和交易请求继续按已有配置处理。[拼多多](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partP/Pinduoduo.lpx) · [闲鱼](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xianyu_splash_ad_block.plugin#L30-L40) |
| 大众点评 | 启动时的开屏配置 | 只匹配列出的启动请求，餐厅推荐、商户优惠和点评正文不在该规则中。[大众点评](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L17-L25) |
| 高德地图、铁路 12306 | 高德的两条启动广告接口，铁路 12306 的独立广告主机 | 路线、导航、查票和购票接口不在名单中。App 自带的开屏倒计时可能继续显示。[高德地图](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partG/AutoNavi.lpx#L27-L36) · [铁路 12306](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/part1/12306.lpx#L14-L22) |

## 内容和影音

**YouTube** 的 Safari 网页助手可单独安装，支持首页和搜索结果里的部分独立广告位，以及普通播放页上已经可点击的「跳过广告」按钮。插件中的 Google 广告域名规则不能保证过滤原生 YouTube App 的片头和中插。独立助手无需开启 HTTPS 解密。[范围与安装](youtube/README.md)

| App | 已实现的规则 | 适用条件与依据 |
| --- | --- | --- |
| 小红书、知乎 | 小红书首页去掉带非空 `ads_info` 对象的广告卡，另拦三台广告素材主机。知乎首页按 `type=feed_advert` 过滤 | 小红书保留仅有商品关联、直播标记的普通条目，知乎保留未知类型。作者自行植入的推广通常没有这类标记。[小红书](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xiaohongshu_splash_ad_block.plugin#L58-L65) · [知乎](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) |
| 哔哩哔哩 App 开屏 | 在 `/x/v2/splash/list` 的成功 JSON 中，素材同时满足 `is_ad=true`、`cm_mark=1` 和有效数值 ID 时才移除。`show`、`keep_ids` 只清理同一响应中仅属于已删广告的数值引用。 | 固定资料中的一条商业素材被识别。独立的品牌图、活动和曝光上报接口继续使用原响应。实际客户端是否使用该路径，仍取决于版本与投放。[开屏响应样本](https://github.com/realysy/bili-apis/blob/3802052be89effc3bbd27574037942310a23672d/docs/APP_widget/splash.md#L321-L351) · [移动端请求观测](https://github.com/UserC23/bilibili-ads-loon/blob/38ad51c6bef2be64625b7a86e9bf8aac44a4119a/docs/analysis.md#L36-L46) |
| 微信、哔哩哔哩 | 公众号文章广告列表、B 站 App 和网页首页推荐、App 混排横幅中的广告子项 | 公众号仅尝试解析声明为 JSON 的成功 HTTP 响应，跳过 HTML 验证页面。保留阅读互动和普通推荐，避免仅凭 `ad_info` 误删视频。[内嵌广告说明](README.md#内嵌广告) |
| 微博主 App | 关注流的 `statuses` 以及首页、推荐流的 `items` 中，只移除带数值 `is_ad=1` 或精确标签 `mblogtypename="广告"` 的微博。另有原有开屏和素材主机规则。 | 普通微博、文字里出现“广告”的正文和未标记推广继续显示。保留正常微博的顺序及分页字段。[广告标记](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L140-L155) · [关注流](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L438-L452) · [首页和推荐](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L96-L102) |
| 微博轻享版 | 在 `api.weibo.cn/2/ad/weibointl` 的成功 JSON 中，仅清空 `data` 广告数组。 | 只匹配这条路径，覆盖取决于当前版本是否使用它。[轻享版专用接口](https://github.com/gj0134/Loon-Plugins/blob/5c835d0db14a4808c19cd010641be1235b6b3d73/plugins/Weibo-Intl-AdBlock.plugin#L7-L16) |
| 酷安 | 在 `api.coolapk.com/v6/main/dataList`、`/v6/main/indexV8` 成功返回的 `data` 数组中，只移除 `entityTemplate="sponsorCard"` 的赞助卡。 | 普通动态、带商品的内容及带“红包”等字样的卡片可正常保留。页面仍可能展示未带该标记的推广。[赞助卡字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/coolapk.js#L28-L44) |
| 网易云音乐、QQ 音乐 | 网易云开屏图片及视频广告素材，QQ 音乐广告投送及素材 | 播放与普通封面 CDN 不在域名拦截中。[网易云](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/NeteaseCloudMusic_ads_v2.lpx#L8-L12) · [QQ 音乐](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/qqmusic_splash_ad_block.plugin#L14-L20) |
| 腾讯视频、优酷、爱奇艺 | 腾讯广点通广告素材主机、优酷两个广告交易主机、爱奇艺规则收录的 Tanx 广告主机 | 覆盖部分外部广告请求。没有对播放清单或视频流动手。与正片拼接播放的广告、口播和未经过这些主机的贴片仍可出现。[腾讯视频](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/tencentvideo_splash_ad_block.plugin#L13-L19) · [优酷](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/youku_splash_ad_block.plugin#L18-L24) · [爱奇艺](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partA/iQIYI.lpx#L15-L23) |

懒人版还涵盖百度、字节穿山甲、快手、Google 和 WPS 等已知广告主机。域名规则、原生复写和完整解密主机名可查看[插件原文](iPad-AdSuite.lpx)。

## 已完成的验证

回归测试使用离线样例核对插件中的实际 URL 正则及 jq 过滤器。购物样例包含错误响应、未知结构、相似操作名、正常商品和优惠券。测试还核对原有规则、正常业务路径及主机名单。真实广告命中率、实际吞吐量和 HTTPS 解密耗时需要在启用后的 iPhone 或 iPad 上验证。在仓库根目录运行 `python -m unittest discover -s tests` 可运行整套离线回归测试。[抖音专项](tests/test_mobile.py) · [微博与酷安](tests/test_social.py) · [美团专项](tests/test_meituan.py) · [购物与常见 App 测试](tests/test_suite.py) · [原内嵌规则测试](tests/test_inline.py)

## 在 iPad 上核对单条规则

- **域名拦截**无需 HTTPS 解密。用 Safari 打开下方的 Google 广告脚本，再到 Loon「仪表 → 请求记录」搜索 `pagead2.googlesyndication.com`。打开刚才的记录，核对策略为 `REJECT`、规则来源为正在验证的插件。Safari 的加载错误本身无法说明由谁拦截。[打开 Google 广告脚本](https://pagead2.googlesyndication.com/tag/js/gpt.js?loon_check=1) · [Google 官方脚本地址说明](https://developers.google.com/publisher-tag/guides/general-best-practices) · [Loon 请求详情的来源字段](https://t.me/LoonNews/706)
- **美团响应复写**适用于已启用懒人版并已为该主机配置 HTTPS 解密的设备。用 Safari 打开下方的公开接口，在 Loon 请求记录中搜索 `queryWechatAdvertisement`，点开同一时间的请求，查看命中的响应复写及其来源「常用 App 去广告（懒人版）」。服务端也可能直接返回空的 `adSiteList`。如要核对条目变化，可仅切换本插件，在同一网络刷新接口，比对停用时出现的 `adunit-…` 广告位和启用后的结果，再恢复原状态。两次都为空则无法通过响应内容判定。[打开美团餐饮微信广告位接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement)
