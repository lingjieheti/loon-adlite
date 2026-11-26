# 逐 App 连接兼容性复核

2026-11-27，以 [大众点评修订后的订阅](https://github.com/lingjieheti/loon-adlite/blob/f9e6f87f53a3a4bf4667f79a90ba432409603409/iPad-AdSuite.lpx) 为基线，核对三个订阅的 82 条精确域名拒绝、41 条懒人版复写和 34 个解密主机，重点比对原始广告规则、业务请求记录及公开技术资料。Loon 的 HTTPS 解密按主机生效。同主机正常请求即使绕过复写，仍可能在设备上解密。下列结果是规则重放和公开样例核验，实际时延、签名请求及客户端重试仍需在 iOS 设备上观测。[Loon 解密说明](https://nsloon.app/docs/MitM/)

## 后续补回的广告位

本轮新增五条精确广告主机规则，覆盖猫眼小程序弹窗和横幅、小红书广告图、1RTB 与 Tanx 广告请求。B 站竖屏推荐使用已列名的同一 App 主机，只处理有明确商业字段且混有正常视频的响应。新版懒人版的解密主机数为 24。[新增广告依据](COVERAGE.md#独立投放主机补漏) · [竖屏广告抓包](https://github.com/UserC23/bilibili-ads-loon/blob/38ad51c6bef2be64625b7a86e9bf8aac44a4119a/docs/analysis.md#L137-L146)

可直接影响业务的候选中，京东曾有拦截共用图片域名导致商品图消失的公开修复，闲鱼开屏素材桶亦用于普通内容视频。飞常准的历史广告主机在两套公开 DNS 中均未解析。本轮补漏按独立广告服务和可识别响应字段取证，原生 App 中仍混在业务响应里的广告覆盖取决于实际投放。[京东商品图记录](https://github.com/Thelongdarkorg/loon-plugins/commit/4f431103128b12ccc3632b9c9b1299b8b933bcd7) · [闲鱼视频架构](https://developer.aliyun.com/article/785838)

## 已调整的应用

| 应用 | 已查证的范围和处理 |
| --- | --- |
| 京东 | 官方文档列出 api.m.jd.com 的登录态关联令牌，新版规则维护者的请求记录显示开屏使用 POST 正文和编码数据。移除了这个共用主机的两条旧版明文复写及解密声明。京媒独立广告、竞价与已核实的网页曝光仍有规则。[京东开发文档](https://opendoc.jd.com/shop/newisv/docs/documents/questionAndAnswer#问题15) · [新版 HAR 记录](https://github.com/zbsdsb/loon-adblock-plugins#为什么京东插件要叫-v2) |
| 拼多多 | 两台 /api/cappuccino/splash 主机匿名返回 HTTP 200 和空广告数据，旧版直接回 404。撤下该条复写及只为它解密的 api.yangkeduo.com。api.pinduoduo.com 仍处理首页和搜索结果，正常订单、客服和物流路径样例绕过复写，仍在主机解密范围内。[订单及客服样例](https://github.com/Reukix/ukix/blob/44daad38c7d9b24379cb969f2a1a89ca49ec3297/Script/Pinduoduo.sgmodule#L373-L389) |
| 抖音 | 公开请求记录曾用 aweme.snssdk.com 获取签名播放地址，旧开屏路径与主机组合来自静态分析。撤下该主机的解密，另外三个 amemv.com 主机继续匹配已知开屏和推荐接口。原生直播、支付和当前版本广告命中需实测。[播放请求记录](https://github.com/Evil0ctal/Douyin_TikTok_Download_API/issues/174) · [旧版分析](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L47) |
| 微信 | 公众号旧脚本用图片 GET 上报已知可见性事件，规则从不限方法收窄为 GET。文章阅读互动、实际兼用 GET 和 POST 的附加上报及已校验主曝光规则各按原匹配范围处理。文章主机仍需要解密才能筛选共用 JSON 里的广告。[原始页面脚本](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/index42f400.js#L1617-L1627) |
| 百度贴吧 | iPhone 上的真实 Loon 请求记录表明帖子正文走 tiebac.baidu.com 的 protobuf。已撤下该主机及历史看图广告复写。[iPhone 请求记录](https://github.com/app2smile/rules/issues/247) |
| 高德地图 | 流量测量和独立记录都见到 m5.amap.com 承载导航和打车相关请求。撤下该主机和依赖它的开屏规则。另一主机仅匹配已知阿里妈妈开屏路径。[导航测量](https://tns.thss.tsinghua.edu.cn/~yangzheng/papers/Zhao-CellTrans-UbiComp2019.pdf) · [打车请求记录](https://gist.github.com/cc166/e00ce5690861f2d9896b404c5cfbe810) |
| 飞常准 | 官方在 app.variflight.com 提供行程、航班与会员页面。撤下该主机及两个广告目录共用的复写。[飞常准出行页面](https://app.variflight.com/trip/) |
| 得物 | app.dewu.com 的官方 App 关联声明包含鉴别和分享路径，公开也有正常商品查询记录。撤下该主机和开屏复写。[App 关联声明](https://app.dewu.com/.well-known/apple-app-site-association) · [商品请求记录](https://github.com/ly1205/dewu_stockx/blob/main/dewu_api_v2.py) |
| 猫眼 | p0.pipi.cn 可直接取得正常影片人物图片。撤下该图床与两处广告目录共用的图片复写。[公开图片样例](https://p0.pipi.cn/basicdata/25bfd6d753706dc7ed8077fa5007898cf9e86.jpg?imageMogr2/thumbnail/2500x2500%3E) |
| 转转 | app.zhuanzhuan.com 同时用于官方二手交易站点与已观测的搜索请求。撤下该主机和开屏复写。[官方站点](https://app.zhuanzhuan.com/) · [搜索请求记录](https://jishuzhan.net/article/1944665716061417473) |
| 广发发现精彩 | static.95508.com 可返回正式业务文件。撤下该主机和两个弹窗目录共用的图片复写。[广发公开 PDF](https://static.95508.com/cgbstatic/POCM/commercialPensionFile/20260710/202607101010403506981409129447.pdf) |

## 其他应用的核验结果

| 应用或入口 | 样例和当前范围 |
| --- | --- |
| 哔哩哔哩 | App 首页和开屏使用 app.bilibili.com，其中也有投币等业务。已分离的 API、gRPC 播放与视频 CDN 继续由原连接处理。后续有起播或 App 操作问题时，应从实际命中主机核对这两类流量。[播放兼容修订](https://github.com/lingjieheti/loon-adlite/pull/26) · [客户端业务记录](https://github.com/pskdje/bilibili-API-collect/blob/main/docs/video/action.md) |
| 微博 | api.weibo.cn 的关注流、推荐流和轻享版广告有精确路径。登录和私信样例不匹配复写，涉及同主机时仍可能解密。[独立客户端记录](https://github.com/Greenleonard/vvebo-fix) |
| 微博轻享版 | 只在 /2/ad/weibointl 的已知成功 JSON 清空广告数组，与微博共用 api.weibo.cn。当前客户端命中需实测。[覆盖说明](COVERAGE.md#内容和影音) |
| 酷安 | api.coolapk.com 的两个首页接口只筛选特定赞助卡。已记录的首页初始化请求不匹配复写，仍可能解密。[首页初始化记录](https://github.com/Coolapk-UWP/Coolapk-API-Collect/blob/main/Coolapk-API/%E4%B8%BB%E9%A1%B5/Tab%20%E5%86%85%E5%AE%B9.md) |
| 小红书 | edith 和 rec 都有首页样本。官方资料还列出 edith 的分享鉴权。鉴权路径与复写分开，同主机仍可能被解密。[官方分享鉴权](https://agora.xiaohongshu.com/doc/js) |
| 知乎 | 只筛选首页推荐中的明确广告类型。站内通知和编辑检查样例不匹配复写，同主机仍可能解密。[编辑权限请求记录](https://github.com/p1lab/zhihu-webbridge-research/blob/main/SKILL.md) |
| 爱奇艺 | cards 主机的首页及搜索和官方频道脚本中两种已识别广告位仍有过滤。正片播放入口的规则由业务回归覆盖；现有样本不证明 iOS 的卡片网关耗时。[官方频道资源](https://www.iqiyi.com/static/js/channel_afbe97b7.56f893f6.js) |
| 美团 | mop.meituan.com 的启动广告数组按形状筛选。匿名探测得到业务错误，客户端命中待实测。[覆盖及上游字段](COVERAGE.md#美团) |
| 美团外卖 | wmapi.meituan.com 的启动配置及两个独立开屏路径仍参与过滤。下单样例不匹配复写；匿名开屏请求返回 403，无法推断登录后行为。[覆盖及上游字段](COVERAGE.md#美团) |
| 美团餐饮小程序 | rms.meituan.com 的广告接口匿名返回一项广告，同时同主机提供收银服务。只过滤已核对标识的广告位，收银页不匹配复写，仍可能解密。[广告接口](https://rms.meituan.com/api/v1/rmsmina/c/queryWechatAdvertisement) · [收银服务](https://rms.meituan.com/shouyin/base) |
| 大众点评 | App 网关、网站及三个共用图床的解密已在上一轮撤下，正常网页和图片样例均可绕过插件。[兼容修订](https://github.com/lingjieheti/loon-adlite/pull/28) |
| 淘宝 | MTOP 网关及已知消息宿主绕过本插件。手机网页保留只匹配特定广告 JSONP GET 的曝光规则。[消息修订](https://github.com/lingjieheti/loon-adlite/pull/27) |
| 菜鸟 | 淘宝共用 MTOP 网关沿用原连接，已知广告复写已撤下。[菜鸟网关记录](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CHANGELOG.md#L24-L27) |
| 闲鱼 | MTOP 交易和消息样例绕过本插件。原开屏广告可能出现。[闲鱼消息团队](https://juejin.cn/post/7005836853001748517) |
| 山姆 | 官方会员协议、购物网关和图床样例在三个订阅均无命中。其他聚合规则处理共用主机曾有购物车异常记录。[专项排查](COVERAGE.md#大众点评和山姆卡顿排查) |
| 快递 100 | 拼多多联盟回调仅限 GET 且浏览器明确标为图片。运单、网页导航和普通请求样例绕过复写。[联盟覆盖](COVERAGE.md#短视频和购物广告监测) |
| BOSS 直聘 | 目前只有启动广告 URL 的规则证据。模拟职位和登录样例不复写，尚无同主机真实人事或聊天捕获；此主机仍在解密名单。[广告路径](COVERAGE.md#更多常用-app-的广告位) |
| 去哪儿 | homefront.qunar.com 匿名开屏探测返回 405，只有历史专用开屏记录，缺少该精确主机的实际订票和支付样本。[广告路径](COVERAGE.md#更多常用-app-的广告位) |
| 掌上京彩 | 仅处理静态广告目录匹配后缀的图片。账单、支付与其他图片样例不匹配复写，尚未核实该静态主机提供其他当前业务。[目录与回归](COVERAGE.md#更多常用-app-的广告位) |
| 大麦 | 通用 MTOP 网关的开屏、门票和下单样例在三个订阅均无命中。[业务回归](tests/test_shopping_apps.py) |
| 淘票票 | 通用 MTOP 的票务广告及订单样例在三个订阅无匹配规则。[业务回归](tests/test_shopping_apps.py) |
| 盒马 | 已核对的 MTOP 样例不匹配现有规则。其他规则包以同一网关做广告过滤的行为需按实际命中核验。[业务回归](tests/test_shopping_apps.py) |
| 顺丰 | 查运单和广告路径邻近样例当前均无复写。[出行及物流回归](tests/test_travel_apps.py) |
| 南航 | 登机牌、支付和广告相似路径样例均无复写。[出行及物流回归](tests/test_travel_apps.py) |
| 贝壳找房 | 启动配置和正常活动的样例均无插件复写。[购物回归](tests/test_shopping_apps.py) |

## 仅有精确域名拦截的覆盖

以下条目以当前订阅中的完整广告主机、已引用的上游与现有正常业务样例为核查依据。域名只匹配列出的主机；这是配置级结论。广告等待、奖励视频与原生客户端的变化仍以请求日志和同场景对照为准。[完整域名规则](iPad-AdLite.lpx) · [规则来源](SOURCES.md)

| 应用或服务 | 核查边界 |
| --- | --- |
| QQ 空间 | 曝光和 SDK 事件主机，与聊天、登录、通知及支付样例区分。[广告监测](COVERAGE.md#微信与-qq-广告监测) |
| 腾讯广告 SDK | 转化、展示及广告素材主机。奖励广告如果复用会受影响。[广告监测](COVERAGE.md#微信与-qq-广告监测) |
| 穿山甲 SDK | 专用广告日志与投放主机。宿主 App 可设超时和失败回调，是否触发兜底需看实机日志。[SDK 开屏接入](https://www.csjplatform.com/supportcenter/5379) |
| 网页广告及 Google DAI | 保留已放行的播放清单主机。个别广告 SDK 与浏览器规则的路径匹配粒度不同。[Google 示例流](https://developers.google.com/ad-manager/dynamic-ad-insertion/streams) · [网页覆盖](COVERAGE.md#网页广告) |
| 百度地图 | 广告投放及配置主机，导航、定位与账号主机有独立保留测试。[百度业务回归](tests/test_content_apps.py) |
| 铁路 12306 | 独立广告主机，与官方网站及票务接口分开。[购物和生活](COVERAGE.md#购物和生活) |
| 米家 | 小米广告 SDK 配置主机，设备及账号服务分开。[资源回归](tests/test_app_ad_resources.py) |
| 同花顺 | 独立广告主机，报价和行情保留样例。[资源回归](tests/test_app_ad_resources.py) |
| LINE | 单独广告素材主机，消息和头像 CDN 分开。[资源回归](tests/test_app_ad_resources.py) |
| 下厨房 | 两个百度联盟主机，菜谱查询及普通内容使用其他入口。[App 规则表](COVERAGE.md#更多常用-app-的广告位) |
| 美图秀秀 | 独立广告请求主机，编辑、登录和图像素材保留样例。[App 规则表](COVERAGE.md#更多常用-app-的广告位) |
| 快手 | 三个广告素材主机，普通视频及直播不在域名集合。[来源说明](SOURCES.md) |
| WPS | 广告接口主机，与文档及云空间主机分开。[来源说明](SOURCES.md) |
| 墨迹天气 | 两个广告主机，天气 API 保留。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 虎扑 | 广告交易主机，与社区、赛事及图片分开。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 百词斩 | 两个广告主机，阅读与登录分开。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 澎湃新闻 | 独立广告主机，正文图、视频和音频使用其他服务。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 七猫免费小说 | 广告 CDN，章节正文分开；同 CDN 奖励素材可能受影响。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 虎嗅 | 独立广告查询主机。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 凤凰新闻 | 独立投放主机。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 网易有道词典 | 独立开屏和广告主机，与查词及口语业务分开。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 讯飞输入法 | 单独广告素材主机，输入和语音服务使用其他入口。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 喜马拉雅 | 两台广告主机，现有样例限开屏及广告组件。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 酷狗音乐 | 广告主机及其备用广告主机；没有近期真机证据说明封锁触发业务重试。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 蜻蜓 FM | 广告投放与素材主机。[应用覆盖](COVERAGE.md#国产-app-的独立广告主机) |
| 网易云音乐 | 广告素材主机，播放接口和正常封面不在清单。[影音覆盖](COVERAGE.md#内容和影音) |
| QQ 音乐 | 独立广告素材与广告投放主机，正常播放样例无匹配。[影音覆盖](COVERAGE.md#内容和影音) |
| 腾讯视频 | 公开来源列为广告素材的主机，正片、广告合流和片中口播的结果取决于实际投放。[影音覆盖](COVERAGE.md#内容和影音) |
| 优酷 | 广告竞价及上游受管广告主机，普通业务样例按其他域名核对。[影音覆盖](COVERAGE.md#内容和影音) |

Safari 可选脚本独立于 Loon 订阅。YouTube 网页助手只观察已识别的广告按钮并在可点击时执行；另一个网页助手仅处理已核对的广告位。两者都有 Chromium 和 WebKit 回归。[YouTube 测试](tests/youtube_browser.py) · [网页测试](tests/web_ads_browser.py)

## 实机怎么查

在同一设备和网络，重复打开同一个页面，切换本插件对照一次。若出现明显差异，在 Loon 请求记录中核对主机、命中规则、分流策略、请求耗时及重试间隔。分享结果时只提供必要的主机和规则名称，删去令牌、完整查询和账号信息。
