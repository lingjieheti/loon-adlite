# 功能与上游来源

每个功能先查已有实现，再核对目标 App 或网页上的具体接口、字段和控件。下表区分了采用的规则、做过的本地适配，以及仅用于对照的资料。

GitHub 每周一北京时间 11:27 排期检查本页直接列出的 GitHub 固定文件。报告比较文件内容，列出与上游默认分支已有差异的项目。官网、Gist 和链接到其他手册的二级来源，仍需随功能更新人工核对。维护时先对照许可、设备权限和相关测试，再将选中的改动合入发布分支。[查看历次比对](https://github.com/lingjieheti/loon-adlite/actions/workflows/review-upstreams.yml)

## Loon 去广告插件

轻量版和合并版共用精确域名清单。内嵌版处理微信和哔哩哔哩的四条响应，合并版也包含这四条。三个插件随本仓库发布，在设备上执行 Loon 原生规则。下表的上游链接用于核对域名、接口和字段，安装插件无需同时订阅这些来源。[轻量版](iPad-AdLite.lpx) · [内嵌版](iPad-InlineAds.lpx) · [合并版](iPad-AdSuite.lpx)

| 功能与适用版本 | 采用的依据与本地适配 |
| --- | --- |
| 广告主机 · 轻量、合并 | 用广告组件核对投放用途，用社区域名表交叉核对。Prebid.js 的 TripleLift 适配器给出了竞价地址，v2ray 的数据列出了部分百度、腾讯和穿山甲主机。本站只拒绝选定的完整主机名。HaGeZi 用于比较清单重叠度。逐项证据和已知网站例外见覆盖说明。[AdGuard 移动广告原表](https://github.com/AdguardTeam/AdguardFilters/blob/1256f5db2a6fe797fc93960ab904e1930f7aeef5/MobileFilter/sections/adservers.txt) · [Prebid 适配器](https://github.com/prebid/Prebid.js/blob/9902b20d730d4b4afb13d09256e059a73f929e70/modules/tripleliftBidAdapter.js#L10) · [v2ray 字节广告主机](https://github.com/v2ray/domain-list-community/blob/564849233e2fa3a33e71a4b02dd51bcc7a9bc1a8/data/bytedance-ads) · [HaGeZi 对照与网站例外](COVERAGE.md#网页广告) |
| 微信公众号 · 内嵌、合并 | NobyDa 的公开实现记录了文章广告接口及计数、列表字段。本站的 jq 只处理识别成功的 JSON，清空广告列表并同步计数，保留文章身份、阅读数和评论等字段。[NobyDa 字段示例](https://github.com/NobyDa/Script/blob/730362a7c51e9a3b4bbc10858d81ccd086f6d7e8/QuantumultX/File/Wechat.js#L24-L28) · [内嵌规则测试](tests/test_inline.py) |
| 哔哩哔哩 · 内嵌、合并 | 对照 Biliverse 的卡片类型和跳转类型，分别处理 App 首页、iPad 混排横幅和网页推荐。开屏另外核对公开响应中的两种商业标记及素材 ID，保留普通素材和仍被使用的引用。[Biliverse 首页卡片](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/process/Response.mjs#L122-L179) · [网页推荐](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/process/Response.mjs#L359-L379) · [开屏样本](https://github.com/realysy/bili-apis/blob/3802052be89effc3bbd27574037942310a23672d/docs/APP_widget/splash.md#L321-L351) |
| 京东、淘宝、菜鸟及其他购物出行 App · 合并 | 对照 fmz200 的京东首页字段、淘宝开屏槽，以及 UserC23 的菜鸟广告接口。本站分别检查操作名、业务状态和响应结构。拼多多、闲鱼、点评和高德只匹配列出的开屏路径。[京东字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/jingdong/jingdong.js#L258-L280) · [淘宝开屏槽](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/myBlockAds.js#L84-L121) · [菜鸟接口](https://github.com/UserC23/cainiao-ads-loon/blob/e6aac018f1a61df72b51a290a4beb99993692b77/CainiaoAds.plugin#L49-L50) · [各 App 路径与来源](COVERAGE.md#购物和生活) |
| 美团、美团外卖、餐饮小程序 · 合并 | 依据上游记录的启动字段和素材目录缩小匹配范围。餐饮小程序还用公开响应核对过广告位标识。菜单、配送费和结算请求不在这些路径中。[主 App 启动字段](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L97-L109) · [外卖启动字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [六条规则的来源与验证](COVERAGE.md#美团) |
| 抖音 · 合并 | 从 Choler 的旧版实现核对推荐流广告标记，从 Belcheck 的旧版 iOS 静态分析核对候选开屏路径。本站仅处理同时包含可识别非广告作品或直播的成功 JSON。当前客户端的实际命中仍待验证。[Choler 字段示例](https://github.com/Choler/Surge/blob/3d9d3ed61676cd0e3f309156e47e60f509ae612a/Script/douyin.js#L27-L43) · [Belcheck 分析](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Docs/DouyinAdClean.md#L25-L65) · [抖音测试边界](COVERAGE.md#抖音主-app) |
| 小红书、知乎、微博、酷安等内容 App · 合并 | 逐个核对首页广告卡、微博广告标记及酷安赞助卡，只从指定数组移除匹配项。腾讯视频、优酷、爱奇艺等现有覆盖来自指定广告主机。视频口播和与正片合流的广告仍可能播放。[知乎广告卡](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/js/zhihu.js#L33-L69) · [微博字段](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Scripts/weibo/weibo_main.js#L140-L155) · [其他内容 App 的来源](COVERAGE.md#内容和影音) |

**许可与使用方式**　所引快照中，Biliverse 和 Prebid.js 标注 Apache-2.0，v2ray、app2smile 和 UserC23 标注 MIT，AdGuardFilters、NobyDa 和 fmz200 标注 GPL-3.0。Choler 的该版本未查到仓库级许可。表内也链接了公开的接口样例、个人使用项目和附有转载限制的资料。本文引用其观测位置，插件中没有引入这些项目的脚本文件。后续如复制代码或过滤表，应按该文件具体版本的授权和署名要求处理。[Biliverse 许可](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/LICENSE) · [app2smile 许可](https://github.com/app2smile/rules/blob/df6366a7024e0b3f0aa3510c5b791eea6f3cba89/LICENSE.md) · [fmz200 许可](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/LICENSE) · [ZenmoFeiShi 使用说明](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/README.md#L7) · [Belcheck 使用说明](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/README.md#L7-L18)

## Safari 网页助手

| 功能 | 采用的依据与本地适配 |
| --- | --- |
| YouTube 网页 | 参考 EasyList 记录的广告卡片层级，按首页、搜索页分别匹配。跳过广告的部分根据 YouTube 播放器实际控件编写，只点击当前可用的官方按钮。[EasyList 固定版本](https://github.com/easylist/easylist/blob/25c34f4d85f863466cf6efb8232bb55a20c6c5fb/easylist/easylist_specific_hide.txt#L8865-L8884) · [YouTube 广告格式](https://support.google.com/youtube/answer/2467968?hl=zh-Hans) |
| Pornhub 网页 | 从 EasyList 选取侧栏广告标识和投放链接前缀，依据 AdGuardFilters 的移动广告位和 TrafficJunky 元素收窄选择器。浏览器应用一张本地样式表。[EasyList 侧栏](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L883) · [EasyList 投放链接](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L1265) · [AdGuardFilters 移动规则](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/MobileFilter/sections/specific_web.txt#L6194-L6200) |

上述广告位规则来自 The EasyList authors 和 AdGuard。EasyList 对其自有规则提供 GPL-3.0-or-later 或 CC BY-SA 3.0-or-later 双重许可，本项目适配的 EasyList 规则片段采用 GPLv3 选项。所引 AdGuardFilters 版本使用 GPLv3，仓库附有许可原文。[EasyList 许可与署名](https://easylist.to/pages/licence.html) · [AdGuardFilters 许可](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/LICENSE) · [随附的 GPLv3 文本](licenses/GPL-3.0.txt)

五个网页助手均从本仓的对应文件更新。Userscripts 可在扩展菜单检查和安装新版，定期检查默认关闭。已安装且没有更新地址的旧脚本需要手动安装一次新版。需要整站元素过滤时，还可选用 AdGuard for iOS。[Userscripts 更新实现](https://github.com/quoid/userscripts/blob/8b743e37dd7dfc8a510aff4e5e2ab8b1cc9210df/xcode/Ext-Safari/Functions.swift#L916-L928) · [默认更新设置](https://github.com/quoid/userscripts/blob/8b743e37dd7dfc8a510aff4e5e2ab8b1cc9210df/src/ext/shared/settings.js#L168-L191) · [AdGuard for iOS 设置](web/README.md)

## 每日签到、领券与提醒

| 功能 | 采用的依据与本地适配 |
| --- | --- |
| 京豆、什么值得买签到 | 京东使用官方卡片结构，并参考 huntingrin（MIT）记录的待签、已签状态。什么值得买使用官网签到入口。两项都在带有专用标记的已登录页面识别按钮，并按日期在本地去重。[京豆实测记录](https://github.com/huntingrin/jd-bean-claim/blob/d07d3a40a92074f73575d4cff4de0367d01aef91/SKILL.md#每日签到) · [京东卡片配置](https://storage.360buyimg.com/assets-fe/mybean/config-js/global.js) · [什么值得买签到说明](https://zhiyou.smzdm.com/user/tequan/) |
| 京东指定券 | 根据京东公开网页组件识别普通单券，按券链接去重。旧电脑版券地址的参数参考公开 SDK 示例。该修订未找到仓库许可证，这里只使用链接格式。[京东网页组件](https://storage.360buyimg.com/miniprogram-platform/m-add-sns/receive-coupon-m/main.a04e4b02.js) · [电脑版链接示例](https://github.com/irebit/jingdong_union_go/blob/deb4c5eaa5c63a08a423ae5d3f24eec432efc30f/jd.union_test.go#L84) |
| 淘宝指定店铺券 | 淘宝开放平台和 OpenFlutter/nautilus（Apache-2.0）提供了店铺、活动两个 ID 的领券链接格式。网页助手根据官方券面判断有效期、门槛和「确认领取」按钮，在同一张券上每天最多尝试一次。[淘宝开放平台](https://developer.alibaba.com/docs/doc.htm?articleId=109022&docType=1&treeId=796) · [OpenFlutter 示例](https://github.com/OpenFlutter/nautilus/blob/787250c0f02002697b6da058a8477159a607ae0f/README.md#L46-L48) · [淘宝券页组件](https://g.alicdn.com/cm/m-rx-coupon/0.1.2/pages/detail/index.web.js) |
| 两款 Loon 提醒 | 京东提醒打开京豆页。三平台提醒在设备上生成通知，用户轻点后打开所选活动。淘宝金币和红包入口分别与 JavisPeng（GPL-3.0）、TonyJiangWJ（GPL-2.0）的 Android 签到流程交叉核对。iOS 使用淘宝公开跳转格式。抖音商城优惠由用户在 App 内领取。两款提醒均使用本仓固定提交的脚本。[淘金币](https://github.com/JavisPeng/taojinbi/blob/e0e9638f48f863c0ddf250ce0ea30df432288dd0/taojinbi.js#L478-L488) · [红包签到](https://github.com/TonyJiangWJ/Unify-Sign/blob/821962e037ae0578f66acff4fc26d37dedac482f/core/Taobao-Sign.js#L53-L69) · [iOS 入口样例](https://gist.github.com/JamesHopbourn/046bc341e7debfd0c86e3b388d983c53/3809a04465599866323dcc8685d64bfa5332e543) · [抖音商城指南](https://apps.apple.com/cn/story/id1759101041) |

签到和单券助手根据官网公开的活动入口、页面结构和控件状态编写。浏览器访问官网并维持登录，助手使用可见按钮。官网发布的前端代码用于核对界面，未收录到本仓。[安装、验证范围与到账说明](checkin/README.md)
