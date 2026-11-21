# 常用 App 合并版的覆盖范围

本页对应 2026-11-21 的 `iPad-AdSuite.lpx`。同一款 App 可能同时使用广告联盟、自己的内容接口及服务端视频插播。以下列出已实现的广告位置，规则数量不能换算为拦截率。

## 购物和生活

| App | 已实现的规则 | 适用条件与保留内容 |
| --- | --- | --- |
| 京东 | 京媒广告请求、另一竞价主机的 `/adx/` 路径。能识别操作名时，清空开屏图和次数，剔除首页两种悬浮推广楼层 | 要求 `start` 或 `welcomeHome` 明确出现在 URL 查询参数中，响应为匹配结构的 JSON。新版可能把操作名及正文编码，此时这两条复写会跳过。商品图片 CDN、比价、优惠券、购物车和订单均未列为拦截目标。[京媒 SDK](https://help-sdk-doc.jd.com/ansdkDoc/faq/faq.html) · [首页字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [竞价接口](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/jd_splash_ad_block.plugin#L19-L25) · [新版样本和限制](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/tests/jd-test.js#L26-L50) |
| 淘宝 | 淘宝开屏配置的 `taobao-splash` 槽，仅移除含图片或视频素材地址的广告条目 | 校验方法名、版本和 MTOP 成功状态。正常首页、红包、商品视频、详情和结算不在复写路径中。首页混排的商业推荐仍可能出现。[淘宝开屏字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/myBlockAds.js#L84-L121) |
| 菜鸟 | 淘宝网关中菜鸟专用广告投放接口的成功响应 | 仅在接口和响应形状吻合时清空广告数据，保留业务状态。没有取得真实成功投放响应。[菜鸟维护者规则](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CainiaoAds.plugin#L49-L50) |
| 拼多多、闲鱼 | 拼多多的开屏配置路径，闲鱼的同步和异步开屏广告方法 | 只匹配指定路径或方法，不封购物网关。商品推荐、优惠和交易请求继续按已有配置处理。[拼多多](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partP/Pinduoduo.lpx) · [闲鱼](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xianyu_splash_ad_block.plugin#L30-L40) |
| 美团、大众点评 | 美团独立广告主机，大众点评启动时的开屏配置 | 不删除餐厅推荐、商户优惠和点评内容。[美团](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan.lpx#L12-L22) · [大众点评](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partD/DianPing.lpx#L17-L25) |
| 高德地图、铁路 12306 | 高德的两条启动广告接口，铁路 12306 的独立广告主机 | 路线、导航、查票和购票接口不在名单中。App 自带的开屏倒计时可能继续显示。[高德地图](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partG/AutoNavi.lpx#L27-L36) · [铁路 12306](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/part1/12306.lpx#L14-L22) |

## 内容和影音

| App | 已实现的规则 | 适用条件与依据 |
| --- | --- | --- |
| 小红书、知乎 | 小红书首页去掉带非空 `ads_info` 对象的广告卡，另拦三台广告素材主机。知乎首页按 `type=feed_advert` 过滤 | 小红书保留仅有商品关联、直播标记的普通条目，知乎保留未知类型。作者自行植入的推广通常没有这类标记。[小红书](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/xiaohongshu_splash_ad_block.plugin#L58-L65) · [知乎](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) |
| 微信、哔哩哔哩 | 公众号文章广告列表、B 站 App 和网页首页推荐、App 混排横幅中的广告子项 | 对齐原内嵌版，保留阅读互动和普通推荐，避免仅凭 `ad_info` 误删视频。[内嵌版说明](README.md#内嵌广告插件) |
| 微博 | 开屏预加载、广告图片、已知广告策略主机 | 只处理列入名单的广告请求。[微博](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/weibo.plugin#L28-L45) |
| 网易云音乐、QQ 音乐 | 网易云开屏图片及视频广告素材，QQ 音乐广告投送及素材 | 播放与普通封面 CDN 不在域名拦截中。[网易云](https://github.com/zbsdsb/loon-adblock-plugins/blob/890f64953efc870d4ca6cc5ec19b048c88ec73bb/NeteaseCloudMusic_ads_v2.lpx#L8-L12) · [QQ 音乐](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/qqmusic_splash_ad_block.plugin#L14-L20) |
| 腾讯视频、优酷、爱奇艺 | 腾讯广点通广告素材主机、优酷两个广告交易主机、爱奇艺规则收录的 Tanx 广告主机 | 覆盖部分外部广告请求。没有对播放清单或视频流动手。与正片拼接播放的广告、口播和未经过这些主机的贴片仍可出现。[腾讯视频](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/tencentvideo_splash_ad_block.plugin#L13-L19) · [优酷](https://github.com/Thelongdarkorg/loon-plugins/blob/2d0443ce1ecec36cf173634e77ba52224efbdc38/youku_splash_ad_block.plugin#L18-L24) · [爱奇艺](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partA/iQIYI.lpx#L15-L23) |

合并版也保留原来的百度、字节穿山甲、快手、Google 和 WPS 等广告主机。抖音有机会命中其中的字节广告服务，尚未验证当前抖音客户端的混排广告可被识别。完整清单和 15 个 HTTPS 解密主机可直接查看[插件原文](iPad-AdSuite.lpx)。

## 已完成的验证

回归测试使用离线样例核对插件中的实际 URL 正则及 jq 过滤器。购物样例包含错误响应、未知结构、相似操作名、正常商品和优惠券。测试还核对原有规则、正常业务路径及主机名单。真实广告命中率、实际吞吐量和 HTTPS 解密耗时需要在启用后的 iPad 上验证。[购物与常见 App 测试](tests/test_suite.py) · [原内嵌规则测试](tests/test_inline.py)
