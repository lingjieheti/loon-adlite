# 功能与上游来源

每个功能先查已有实现，再核对目标 App 或网页上的具体接口、字段和控件。下表区分了采用的规则、做过的本地适配，以及仅用于对照的资料。

GitHub Actions 每天北京时间 12:17 排期检查京东、腾讯和优酷的广告域名。同步程序核对上游 MIT 许可，只选择指定分类中带有 `@ads` 标记、且在本仓已审核名单中的完整主机名。每轮审计都从同一上游提交重新计算名单，对照两份订阅，并运行插件、隐私和浏览器测试。有变化且通过全部检查时才自动发布到 `main`。名单未变时保留原订阅，运行摘要会记录本次核对的上游版本。App 内嵌广告的 HTTPS 主机和响应复写由维护者另行审核。[自动更新记录](https://github.com/lingjieheti/loon-adlite/actions/workflows/sync-ad-hosts.yml) · [筛选条件](.github/scripts/sync_ad_hosts.py) · [京东](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/jd) · [腾讯](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/tencent) · [优酷](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/youku) · [上游 MIT 许可](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/LICENSE)

GitHub 每天北京时间 11:27 排期比对本页和覆盖说明（COVERAGE.md）引用的固定版本 GitHub 文件。报告列出已变化、已移除和未能核对的文件，供维护者逐项复核。官网、Gist 等其他来源随功能更新人工核对。维护时先对照许可、设备权限和相关测试，再将选中的改动合入发布分支。[查看历次比对](https://github.com/lingjieheti/loon-adlite/actions/workflows/review-upstreams.yml)

## Loon 去广告插件

轻量版和合并版共用精确域名清单。内嵌版的七条原生复写包括四条内容过滤和三条公众号广告监测规则，合并版全部包含。三个插件随本仓库发布，在设备上执行 Loon 原生规则。下表的上游链接用于核对域名、接口和字段，安装插件无需同时订阅这些来源。[轻量版](iPad-AdLite.lpx) · [内嵌版](iPad-InlineAds.lpx) · [合并版](iPad-AdSuite.lpx)

| 功能与适用版本 | 采用的依据与本地适配 |
| --- | --- |
| 广告主机 · 轻量、合并 | 用广告组件核对投放用途，用社区域名表交叉核对。Prebid.js 的 TripleLift 适配器给出了竞价地址，v2ray 的数据列出了部分百度、腾讯和穿山甲主机。本站只拒绝选定的完整主机名。HaGeZi 用于比较清单重叠度。逐项证据和已知网站例外见覆盖说明。[AdGuard 移动广告原表](https://github.com/AdguardTeam/AdguardFilters/blob/1256f5db2a6fe797fc93960ab904e1930f7aeef5/MobileFilter/sections/adservers.txt) · [Prebid 适配器](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/tripleliftBidAdapter.js#L10) · [v2ray 字节广告主机](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/bytedance-ads) · [HaGeZi 对照与网站例外](COVERAGE.md#网页广告) |
| 微信公众号 · 内嵌、合并 | NobyDa 的公开实现记录了文章广告接口及计数、列表字段。本站的 jq 只处理识别成功的 JSON，清空广告列表并同步计数，保留文章身份、阅读数和评论等字段。[NobyDa 字段示例](https://github.com/NobyDa/Script/blob/730362a7c51e9a3b4bbc10858d81ccd086f6d7e8/QuantumultX/File/Wechat.js#L24-L28) · [内嵌规则测试](tests/test_inline.py) |
| 哔哩哔哩 · 内嵌、合并 | 对照 Biliverse 的卡片类型和跳转字段过滤 App 首页与 iPad 混排横幅。开屏只处理有明确商业标记和素材 ID 的条目。维护者公开的 iOS 客户端 9.16.x 记录表明，网页推荐所在的 `api.bilibili.com` 也提供播放地址和视频详情。另有客户端 9.7.0 的实测记录使用独立的 `grpc.biliapi.net` 播放接口。两份订阅均保留这些播放主机的原连接。[首页卡片](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/process/Response.mjs#L122-L179) · [开屏样本](https://github.com/realysy/bili-apis/blob/3802052be89effc3bbd27574037942310a23672d/docs/APP_widget/splash.md#L321-L351) · [9.16.x 抓包分析](https://github.com/UserC23/bilibili-ads-loon/blob/38ad51c6bef2be64625b7a86e9bf8aac44a4119a/docs/analysis.md#L241-L253) · [9.7.0 播放接口记录](https://github.com/V1Eerie/bilibili-accelerator-loon/blob/7ecfda43d545c2fa9cf4006af145d6d9ef243343/README.md#L92-L98) |
| 京东及其他购物出行 App · 合并 | 对照 fmz200 的京东首页字段，校验操作名、业务状态和响应结构。拼多多按明确的首页模块名筛选广告。大众点评有独立广告域名和网页版品牌广告过滤，高德按列出的开屏路径匹配。淘宝、菜鸟和闲鱼的共用 MTOP 网关优先保障业务连接。[京东字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [各 App 路径与来源](COVERAGE.md#购物和生活) |
| 美团、美团外卖、餐饮小程序 · 合并 | 依据上游记录的启动字段和素材目录缩小匹配范围。餐饮小程序还用公开响应核对过广告位标识。菜单、配送费和结算请求不在这些路径中。[主 App 启动字段](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L97-L109) · [外卖启动字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [六条规则的来源与验证](COVERAGE.md#美团) |
| 抖音 · 合并 | 从 Choler 的旧版实现核对推荐流广告标记，从 Belcheck 的旧版 iOS 静态分析核对候选开屏路径。本站仅处理同时包含可识别非广告作品或直播的成功 JSON。当前客户端的实际命中仍待验证。[Choler 字段示例](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Script/douyin.js#L27-L43) · [Belcheck 分析](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L65) · [抖音测试边界](COVERAGE.md#抖音主-app) |
| 小红书、知乎、微博、酷安等内容 App · 合并 | 逐个核对首页广告卡、微博广告标记及酷安赞助卡，只从指定数组移除匹配项。腾讯视频和优酷的规则针对特定广告主机。爱奇艺另按首页、搜索卡片的广告标记以及官方频道资源记录的展示位过滤。视频口播和与正片合流的广告仍可能播放。[知乎广告卡](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) · [微博字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L140-L155) · [其他内容 App 的来源](COVERAGE.md#内容和影音) |

米家、同花顺系、LINE、百度地图、下厨房和美图秀秀采用完整广告主机名。贴吧、得物、猫眼、转转、BOSS 直聘、去哪儿、飞常准和两个信用卡 App 按独立广告路径或响应字段处理。信用卡 App 的适配限定为静态主机上特定广告目录的图片。每个 App 的来源链接均指向固定的 GitHub 文件版本，由每日来源比对任务追踪。[逐项广告位置与上游证据](COVERAGE.md#更多常用-app-的广告位)

微信公众文章的监测规则依据存档页面脚本中的请求和回调独立编写，并核对了请求封装附加的 `devicetype`、`clientversion`、`x5` 和 `f` 参数。[公共参数](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/tmpl42f400.js#L342-L350) · [GET 请求组装](https://github.com/pomestyle/Weixin_Pilgrim/blob/e58122cef49c3668782623c82ba9fc1e405d491a/src/main/resources/static/fhdf/tmpl42f400.js#L396-L406)

QQ 空间的范围来自维护者的抓包记录，曝光及 SDK 上报主机另与 AWAvenue 的域名表核对。三个主机和微信规则都由 Loon 在本机处理。[逐项请求、返回值与放行范围](COVERAGE.md#微信与-qq-广告监测) · [曝光上报域名](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L735) · [SDK 上报域名](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L776)

腾讯 iOS 转化追踪 SDK 的下载文件在本次复核时的 SHA-256 为 `12d6d9499fd5e7af13e054beb677ab6f5ba60d181e53b4c2c7ce873db7f4f2e7`。核对归档内 `libGDTTrackSDK.a` 记录的转化地址即可验证设备端用途；订阅仅发布精确主机名。[接入说明](https://qzonestyle.gtimg.cn/open_proj/gdt_gw/cms/uploads/ios-sdk-v1.4.pdf) · [腾讯官方归档](https://imgcache.qq.com/qzone/biz/gdt/dev/sdk/ios/release/GDT_iOS_Track_SDK.zip)

**许可与使用方式**　所引快照中，Biliverse 和 Prebid.js 标注 Apache-2.0，v2ray、app2smile 和 UserC23 标注 MIT，AdGuardFilters、NobyDa 和 fmz200 标注 GPL-3.0。Choler 的该版本未查到仓库级许可。表内也链接了公开的接口样例、个人使用项目和附有转载限制的资料。本文引用其观测位置，插件中没有引入这些项目的脚本文件。后续如复制代码或过滤表，应按该文件具体版本的授权和署名要求处理。[Biliverse 许可](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/LICENSE) · [app2smile 许可](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/LICENSE.md) · [fmz200 许可](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/LICENSE) · [ZenmoFeiShi 使用说明](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/README.md#L7) · [Belcheck 使用说明](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/README.md#L7-L18)

常用国产 App 的广告主机逐项核对了 App 专用规则与域名分类。生活、资讯、教育和音频类规则都只选择完整主机名。易车的同一主机上有需要放行的城市和广告回调路径，故本次保留其网络请求。使用者可在覆盖表查到每个广告位或广告主机的固定出处。[国产 App 独立广告主机](COVERAGE.md#国产-app-的独立广告主机) · [易车路径例外](https://github.com/easylist/easylistchina/blob/560a345168f36ca2bfbbf3280b0037451d6e3c80/easylistchina.txt#L15438-L15439)

生活和资讯 App 的主机分类另与 anti-AD 的 MIT 许可快照及 vokins/ad 的 GPL-2.0 许可快照核对。两份上游整表均无需装入 Loon。[anti-AD 许可](https://github.com/privacy-protection-tools/anti-AD/blob/c1d0a1ddb1a5d048f104e2a7eac991b43c3cca8f/LICENSE) · [vokins/ad 许可](https://github.com/vokins/ad/blob/5f177915e12fbaed055dd2ef79f56b97f689ac58/LICENSE)

### 短视频和购物广告监测的来源

穿山甲采用 AWAvenue 列出的两个完整日志主机。该项目的用户也在趣智校园及其支付宝小程序的广告清单里记录了这两个主机。[穿山甲主机](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/3b96f6337ee05400d5be302f7e9bdd5188839b82/Filters/AWAvenue-Ads-Rule-Loon.module#L549-L550) · [用户提交的广告主机记录](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/issues/193)

淘宝手机网页首页脚本 3.3.45 含两条轮播广告样例。`apearAD` 在展示时读取 `args.ifs`，其 JSONP 帮助函数追加回调名。主动点按使用另一个字段 `targetUrl`。复核该文件时 SHA-256 为 `8339e20400dea06004b67ce15ddb0b243096f917404e56c6723b1f43e211620a`。京东的公开搜索样例也分别列出曝光和点击地址，网页请求记录显示 `np` 由图片加载发起。Loon 的 `reject_img(200)` 会在本机返回 1×1 GIF。[淘宝首页脚本](https://g.alicdn.com/dinamic/h5-tb-home/3.3.45/index.min.js) · [京东曝光与点击样例](https://github.com/justoneapi-official/justoneapi-python/blob/fe5fb527f8b1b791635957d24280290155601a4c/docs/api-examples/getApiJdSearchItemListV2.json#L4360-L4361) · [浏览器网络记录，第 125 页](https://internet.hactcm.edu.cn/fileservice/network/file/2024/2/26/133534299256773962.pdf#page=125) · [Loon 原生动作](https://nsloon.app/docs/Rewrite/rewrite_v2/)

拼多多联盟的端点取自快递 100 适配，AdGuard 维护者另记录了该广告主机。本项目只取这条回调路径，并要求浏览器发送图片请求标记，以保留同一地址上的导航和其他用途。GitHub 文件使用固定提交，每日参与来源比对。官网脚本、课堂抓包和讨论跟帖在改动相应规则时复核。[联盟回调路径](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partK/KuaiDi100.lpx#L154-L158) · [维护者跟帖](https://github.com/AdguardTeam/AdguardFilters/issues/225770#issuecomment-4045419446) · [逐项覆盖](COVERAGE.md#短视频和购物广告监测)

## Safari 网页助手

| 功能 | 采用的依据与本地适配 |
| --- | --- |
| YouTube 网页 | 参考 EasyList 记录的广告卡片层级，按首页、搜索页分别匹配。跳过广告的部分根据 YouTube 播放器实际控件编写，只点击当前可用的官方按钮。[EasyList 固定版本](https://github.com/easylist/easylist/blob/25c34f4d85f863466cf6efb8232bb55a20c6c5fb/easylist/easylist_specific_hide.txt#L8865-L8884) · [YouTube 广告格式](https://support.google.com/youtube/answer/2467968?hl=zh-Hans) |
| Pornhub 网页 | 从 EasyList 选取侧栏广告标识和投放链接前缀，依据 AdGuardFilters 的移动广告位和 TrafficJunky 元素收窄选择器。浏览器应用一张本地样式表。[EasyList 侧栏](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L883) · [EasyList 投放链接](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L1265) · [AdGuardFilters 移动规则](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/MobileFilter/sections/specific_web.txt#L6194-L6200) |

上述广告位规则来自 The EasyList authors 和 AdGuard。EasyList 对其自有规则提供 GPL-3.0-or-later 或 CC BY-SA 3.0-or-later 双重许可，本项目适配的 EasyList 规则片段采用 GPLv3 选项。所引 AdGuardFilters 版本使用 GPLv3，仓库附有许可原文。[EasyList 许可与署名](https://easylist.to/pages/licence.html) · [AdGuardFilters 许可](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/LICENSE) · [随附的 GPLv3 文本](licenses/GPL-3.0.txt)

YouTube 和网页去广告助手均从本仓的对应文件更新。Userscripts 可在扩展菜单检查和安装新版，定期检查默认关闭。已安装且没有更新地址的旧脚本需要手动安装一次新版。需要整站元素过滤时，还可选用 AdGuard for iOS。[Userscripts 更新实现](https://github.com/quoid/userscripts/blob/8b743e37dd7dfc8a510aff4e5e2ab8b1cc9210df/xcode/Ext-Safari/Functions.swift#L916-L928) · [默认更新设置](https://github.com/quoid/userscripts/blob/8b743e37dd7dfc8a510aff4e5e2ab8b1cc9210df/src/ext/shared/settings.js#L168-L191) · [AdGuard for iOS 设置](web/README.md)
