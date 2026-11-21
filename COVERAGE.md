# 常用 App 去广告的覆盖范围

本页对应 2026-11-21 的「常用 App 去广告」。iPhone 与 iPad 使用同一订阅文件 `iPad-AdSuite.lpx`，共 39 条精确域名规则、27 条原生复写和 27 个精确 HTTPS 解密主机。同一款 App 可能同时使用广告联盟、自己的内容接口及服务端视频插播。以下列出已实现的广告位置，规则数量不能换算为拦截率。

## 抖音主 App

这两条规则针对中国版抖音主 App 的推荐流和候选开屏路径。2026-11-21 查到的中国区 App Store 版本为 **41.2.0**。上游分析的是 iOS **30.3.0** 的安装包，测试使用合成响应；更早的字段实现只标注支持到 16.2.0。目前缺少 41.2.0 的 iPhone 或 iPad 广告响应和实机命中记录，实际使用的主机、路径和编码可能已经变化。抖音极速版及国际版 TikTok 另用各自客户端。[中国区 App Store](https://apps.apple.com/cn/app/id1142110895) · [30.3.0 静态证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L53) · [旧版适配说明](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Module/douyin.sgmodule#L1-L15)

- **主机范围**仅为 `api3-core-c.amemv.com`、`api3-normal-c.amemv.com`、`api.amemv.com`、`aweme.snssdk.com`。这些是共享 API 主机。开启解密后，发往这些主机的其他 HTTPS 请求也可能在本机经过 TLS 解密；插件只在指定路径执行复写。
- **推荐信息流**仅匹配 `/aweme/v1/feed` 和 `/aweme/v2/feed`。HTTP 200 的 JSON 还须包含数值 `status_code=0` 和顶层 `aweme_list` 数组。混合列表中，只去掉直接条目里 `is_ads` 为布尔 `true` 或数值 `1` 的对象，纯广告页保留，以降低连续翻页遇到空列表的风险。普通视频、直播、带货和本地生活卡片本身均不作为广告依据，其他条目顺序、分页游标和预取字段保留。[历史广告标记](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Script/douyin.js#L27-L43)
- **定向请求与编码**。查询中带 `aweme_id` 或 `aweme_ids` 的定向内容、分享及其他视频路径跳过处理；Protobuf、其他二进制响应和未知 JSON 结构也跳过。这样的请求仍可能携带广告。[上游数据格式边界](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L47-L65)
- **候选开屏接口**共有五个完整路径，分别为`/api/ad/v1/splash/stock`、`/api/ad/v16/splash/preload`、`/api/ad/splash/stock/realtime/v14`、`/api/ad/splash/stock/realtime/v15`、`/api/ad/splash/aweme/v15`。路径出自旧安装包；与前述四个主机的组合是基于静态配置的预防性匹配，缺少各组合的运行时捕获。拒绝请求后仍可能有本地倒计时、缓存画面或重试等待。[候选路径与证据](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/DouyinAdClean.snippet#L9-L17)

## 美团

美团部分包含 6 条原生复写，涉及 6 个完整主机名。美团的独立广告主机继续由域名规则拦截。[域名依据](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan.lpx#L12-L22)

| 场景 | 规则匹配与处理 | 验证边界 |
| --- | --- | --- |
| 美团主 App 开屏 | `mop.meituan.com/api/entryModule/startupPicture`。在匹配的 JSON 中，只清空 `resource` 或 `resourcesMap` 下名为 `startupPicArea` 的数组，兼容相应对象位于顶层或 `data` 中的结构。 | 上游注明适配 12.67.403。当前 iPad 客户端尚无实机命中记录。首页其他弹窗和分发路径可能继续显示。[上游版本](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L1-L3) · [请求路径](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.snippet#L60-L63) · [结构](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L97-L109) |
| 美团外卖 App 开屏 | `wmapi.meituan.com/api/v7/loadInfo` 的已识别 JSON 中，只清空 `data.startpicture.ad` 广告数组。另用一条规则处理同主机 `/api/v7/openscreen`、`/api/v7/startpicture` 两个专用路径。 | `loadInfo` 的其他启动配置和 `mk` 字段保留。外卖首页推荐、商户菜单、配送费和订单各有自己的业务接口。外卖 App 的客户端版本与主 App 分开计算。[开屏字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [三个外卖路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) |
| 美团餐饮微信小程序 | `rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement` 的成功响应中，只移除 `data.adSiteList` 内 `adSiteId` 符合 `adunit-…` 格式的条目，后缀限非空的英文字母、数字、下划线或连字符。 | 核查时匿名访问返回 HTTP 200、`code=200`、`success=true`，其中一个广告位经规则处理后变为零个，其他字段一致。这项结果来自公开接口响应。餐饮小程序的结账、企业餐和优惠权益不能用这条结果推断。[公开接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement) · [路径来源](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L19-L27) |
| 广告素材 | 一条规则匹配 `p0.meituan.net` 和 `p1.meituan.net` 的 `/adunion/`，另一条匹配 `img.meituan.net/bizad/bizad_brandCpt_数字.jpg`，以及该主机 `/adunion/` 目录内以 `.gif.webp` 或 `.jpg.webp` 结尾的素材。 | 同主机上其他目录的商户、菜品和评价图片不会命中这两条规则。素材请求被拦后，客户端仍可能留下占位或等待重试。[p0/p1 目录](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/MeituanAppAdMedia.snippet#L4-L7) · [品牌图文件名](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) · [img 素材后缀](https://github.com/zirawell/R-Store/blob/d0f4dd305bade7cc6a38e3445a768d72aaea0e5b/Rule/QuanX/Adblock/App/M/%E7%BE%8E%E5%9B%A2/rewrite/meituan.conf#L4) |

上述 6 个主机承载的其他 HTTPS 请求也可能在本机经过 TLS 解密。网络耗时、缓存条件和 App 实现都会影响实际体验。菜单图片、结算页或优惠券出现异常时，可停用合并版，在同一网络重复打开相同页面，比对两次结果。[Loon 解密范围](https://nsloon.app/docs/MitM/)

## 购物和生活

| App | 已实现的规则 | 适用条件与保留内容 |
| --- | --- | --- |
| 京东 | 京媒广告请求、另一竞价主机的 `/adx/` 路径。能识别操作名时，清空开屏图和次数，剔除首页两种悬浮推广楼层 | 要求 `start` 或 `welcomeHome` 明确出现在 URL 查询参数中，响应为匹配结构的 JSON。新版可能把操作名及正文编码，此时这两条复写会跳过。商品图片 CDN、比价、优惠券、购物车和订单均未列为拦截目标。[京媒 SDK](https://help-sdk-doc.jd.com/ansdkDoc/faq/faq.html) · [首页字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [竞价接口](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/jd_splash_ad_block.plugin#L19-L25) · [新版样本和限制](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/tests/jd-test.js#L26-L50) |
| 淘宝 | 淘宝开屏配置的 `taobao-splash` 槽，仅移除含图片或视频素材地址的广告条目 | 校验方法名、版本和 MTOP 成功状态。正常首页、红包、商品视频、详情和结算不在复写路径中。首页混排的商业推荐仍可能出现。[淘宝开屏字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/myBlockAds.js#L84-L121) |
| 菜鸟 | 淘宝网关中菜鸟专用广告投放接口的成功响应 | 仅在接口和响应形状吻合时清空广告数据，保留业务状态。没有取得真实成功投放响应。[菜鸟维护者规则](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CainiaoAds.plugin#L49-L50) |
| 拼多多、闲鱼 | 拼多多的开屏配置路径，闲鱼的同步和异步开屏广告方法 | 只匹配指定路径或方法，不封购物网关。商品推荐、优惠和交易请求继续按已有配置处理。[拼多多](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partP/Pinduoduo.lpx) · [闲鱼](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xianyu_splash_ad_block.plugin#L30-L40) |
| 大众点评 | 启动时的开屏配置 | 只匹配列出的启动请求，餐厅推荐、商户优惠和点评正文不在该规则中。[大众点评](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L17-L25) |
| 高德地图、铁路 12306 | 高德的两条启动广告接口，铁路 12306 的独立广告主机 | 路线、导航、查票和购票接口不在名单中。App 自带的开屏倒计时可能继续显示。[高德地图](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partG/AutoNavi.lpx#L27-L36) · [铁路 12306](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/part1/12306.lpx#L14-L22) |

## 内容和影音

| App | 已实现的规则 | 适用条件与依据 |
| --- | --- | --- |
| 小红书、知乎 | 小红书首页去掉带非空 `ads_info` 对象的广告卡，另拦三台广告素材主机。知乎首页按 `type=feed_advert` 过滤 | 小红书保留仅有商品关联、直播标记的普通条目，知乎保留未知类型。作者自行植入的推广通常没有这类标记。[小红书](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xiaohongshu_splash_ad_block.plugin#L58-L65) · [知乎](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) |
| 微信、哔哩哔哩 | 公众号文章广告列表、B 站 App 和网页首页推荐、App 混排横幅中的广告子项 | 对齐原内嵌版，保留阅读互动和普通推荐，避免仅凭 `ad_info` 误删视频。[内嵌版说明](README.md#内嵌广告插件) |
| 微博主 App | 关注流的 `statuses` 以及首页、推荐流的 `items` 中，只移除带数值 `is_ad=1` 或精确标签 `mblogtypename="广告"` 的微博。另有原有开屏和素材主机规则。 | 普通微博、文字里出现“广告”的正文和未标记推广继续显示。保留正常微博的顺序及分页字段。[广告标记](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L140-L155) · [关注流](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L438-L452) · [首页和推荐](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L96-L102) |
| 微博轻享版 | 在 `api.weibo.cn/2/ad/weibointl` 的成功 JSON 中，仅清空 `data` 广告数组。 | 只匹配这条路径，覆盖取决于当前版本是否使用它。[轻享版专用接口](https://github.com/gj0134/Loon-Plugins/blob/5c835d0db14a4808c19cd010641be1235b6b3d73/plugins/Weibo-Intl-AdBlock.plugin#L7-L16) |
| 酷安 | 在 `api.coolapk.com/v6/main/dataList`、`/v6/main/indexV8` 成功返回的 `data` 数组中，只移除 `entityTemplate="sponsorCard"` 的赞助卡。 | 普通动态、带商品的内容及带“红包”等字样的卡片可正常保留。页面仍可能展示未带该标记的推广。[赞助卡字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/coolapk.js#L28-L44) |
| 网易云音乐、QQ 音乐 | 网易云开屏图片及视频广告素材，QQ 音乐广告投送及素材 | 播放与普通封面 CDN 不在域名拦截中。[网易云](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/NeteaseCloudMusic_ads_v2.lpx#L8-L12) · [QQ 音乐](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/qqmusic_splash_ad_block.plugin#L14-L20) |
| 腾讯视频、优酷、爱奇艺 | 腾讯广点通广告素材主机、优酷两个广告交易主机、爱奇艺规则收录的 Tanx 广告主机 | 覆盖部分外部广告请求。没有对播放清单或视频流动手。与正片拼接播放的广告、口播和未经过这些主机的贴片仍可出现。[腾讯视频](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/tencentvideo_splash_ad_block.plugin#L13-L19) · [优酷](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/youku_splash_ad_block.plugin#L18-L24) · [爱奇艺](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partA/iQIYI.lpx#L15-L23) |

合并版还涵盖百度、字节穿山甲、快手、Google 和 WPS 等已知广告主机。域名规则、原生复写和完整解密主机名可查看[插件原文](iPad-AdSuite.lpx)。

## 已完成的验证

回归测试使用离线样例核对插件中的实际 URL 正则及 jq 过滤器。购物样例包含错误响应、未知结构、相似操作名、正常商品和优惠券。测试还核对原有规则、正常业务路径及主机名单。真实广告命中率、实际吞吐量和 HTTPS 解密耗时需要在启用后的 iPhone 或 iPad 上验证。在仓库根目录运行 `python -m unittest discover -s tests` 可运行整套离线回归测试。[抖音专项](tests/test_mobile.py) · [微博与酷安](tests/test_social.py) · [美团专项](tests/test_meituan.py) · [购物与常见 App 测试](tests/test_suite.py) · [原内嵌规则测试](tests/test_inline.py)
