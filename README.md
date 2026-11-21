# 常用 App 去广告

**[在 iPhone 或 iPad 上用 Loon 安装](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [插件原文](iPad-AdSuite.lpx) · [按 App 查看覆盖与依据](COVERAGE.md)

iPhone 和 iPad 共用一份订阅 `iPad-AdSuite.lpx`。原订阅地址指向本仓库 `main` 分支的设备，在 Loon 刷新原插件即可。之前导入的是固定提交或本地文件时，请用上方链接导入一次，启用后关闭旧条目。两台设备可各自从同一地址安装。

1. 在设备上用 Safari 打开上方链接，在 Loon 确认并启用「常用 App 去广告」。如未唤起 Loon，在「配置 → 插件 → ＋」粘贴[订阅原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)。
2. 使用分流模式即可启用 **39 条精确域名规则**。要启用 **27 条原生复写**，需使用 Loon 3.5.1 (978) 或更新版，在该设备开启复写和 HTTPS 解密，并信任自己的 Loon CA。已有证书的设备可沿用当前配置。[Loon 解密文档](https://nsloon.app/docs/MitM/) · [Apple 证书信任设置](https://support.apple.com/zh-cn/102390)
3. 如果还装有下方的基础版或内嵌版，启用合并版后可将它们关闭，避免重复匹配。

## 覆盖与使用体验

- **抖音主 App** 新增实验规则，尝试移除混合推荐页中带明确广告标记的视频，并拦截已知开屏候选路径。上游来自 iOS 30.3.0 的静态分析；核查时中国区公开版本为 41.2.0，当前版实机命中尚未确认。[抖音规则边界](COVERAGE.md#抖音主-app)
- **微博、微博轻享版、酷安** 增加关注或推荐流中明确的广告、轻享版独立广告接口，以及酷安赞助卡处理。[内容和影音](COVERAGE.md#内容和影音)
- **美团主 App、外卖 App、餐饮微信小程序** 分别处理开屏配置、微信广告位和已知广告素材。京东、淘宝、拼多多、闲鱼、菜鸟等购物 App 另有针对性规则。[美团](COVERAGE.md#美团) · [购物和生活](COVERAGE.md#购物和生活)

规则随文件提供，无远程脚本。合并版为 **27 个完整主机名**声明 HTTPS 解密，包括抖音推荐接口、购物 API 和美团共享图片主机。Loon 可能在本机解密这些主机的其他流量，再按路径执行复写。TLS 握手、读取响应和 JSON 处理都可能增加等待时间，实际耗时取决于设备、网络和其他插件，目前没有 iPhone 或 iPad 实机测速结果。

验证时可在相同 Wi-Fi 下先后启用和停用，对比同一家餐厅的菜单图片、同一商品的价格和优惠券，或连续翻页并播放普通视频。如果出现空白、播放停顿、图片缺失或重试增多，可先停用合并版再打开同一页面；偏好避免 HTTPS 解密时可选基础版。

<details>
<summary>美团开屏、小程序与广告素材的匹配依据</summary>

| 美团使用场景 | 本版处理位置 |
| --- | --- |
| 美团主 App | 在匹配的开屏响应中清空 `startupPicArea` 素材数组。主 App 的字段依据来自 12.67.403，目前尚无该规则在 iPad 客户端的实机命中记录。[开屏处理依据](https://github.com/ZenmoFeiShi/Qx/blob/5df3cafc468419e7b58b0f4a1b75df0786ab1c67/MT.js#L127-L135) |
| 美团外卖 App | 在 `loadInfo` 里清空开屏广告数组，另拦截两个专用开屏接口。启动配置中的其他信息继续交给 App 使用。[广告字段](https://github.com/blackmatrix7/ios_rule_script/blob/0b6897dc17e0c513d25449c935a9694818e32f0c/script/startup/startup.js#L76-L87) · [开屏接口](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) |
| 美团餐饮微信小程序 | 在匹配接口的 `data.adSiteList` 中移除符合 `adunit-…` 格式的微信广告位。核对时，公开响应中的一个广告位被移除，其余字段一致。[小程序与素材规则说明](COVERAGE.md#美团) |

素材拦截只匹配 `p0.meituan.net`、`p1.meituan.net` 的 `/adunion/` 目录，以及 `img.meituan.net` 上特定命名的品牌广告图和 `/adunion/` 目录下以 `.gif.webp` 或 `.jpg.webp` 结尾的素材。这三个主机也承载商家、商品和评价图片，插件按路径区分。[广告素材目录](https://github.com/belcheckyoung/Belcheck-QX-AdBlock/blob/12a4f9a5d21dd7efbf35b6b4d0e7e28889d6d24c/Rewrite/MeituanAppAdMedia.snippet#L4-L7) · [品牌广告图](https://github.com/fmz200/wool_scripts/blob/7bc19e8b57b4a67ecefade790574472de69074d0/Loon/plugin/split/partM/Meituan-MeituanWaimai.lpx#L12-L16) · [素材文件名后缀](https://github.com/zirawell/R-Store/blob/d0f4dd305bade7cc6a38e3445a768d72aaea0e5b/Rule/QuanX/Adblock/App/M/%E7%BE%8E%E5%9B%A2/rewrite/meituan.conf#L4)

</details>

## 基础版和内嵌版

基础插件按 22 个完整主机名拦截广告请求，约 1.1 KiB。另有一个可选的内嵌广告插件，针对与正常内容一起下发的广告，使用 Loon 原生 JSON 复写。两者可一起使用，均不加载远程脚本。

[安装基础插件](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [安装内嵌广告插件](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [基础插件原文](iPad-AdLite.lpx) · [内嵌插件原文](iPad-InlineAds.lpx)

## 内嵌广告插件

| 使用场景 | 处理内容 | 保留内容 |
| --- | --- | --- |
| 微信公众号文章 | 清空广告接口或阅读互动接口返回的广告列表，并把对应计数归零 | 正文、阅读数、点赞和其他互动字段 |
| 哔哩哔哩 App 首页 | 根据卡片类型和跳转类型共同识别广告卡，移除混排横幅中标记为广告的子项 | 普通视频、直播、活动横幅和未知卡片，保持原顺序 |
| 哔哩哔哩网页首页 | 移除推荐列表中明确标注为广告的卡片 | 带广告位元数据的普通视频和分页信息 |

在设备上用 Safari 点「安装内嵌广告插件」，确认导入并启用「iPad 内嵌广告过滤」。已有基础版可以继续使用。若链接未唤起 Loon，可在「配置 → 插件 → ＋」粘贴[内嵌插件原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)。

**使用条件**　Loon 3.5.1 (978) 或更新版，已开启复写和 HTTPS 解密，并在该设备上信任自己的 Loon CA。如果设备还没有 CA，可使用 Loon 官方证书工具在本机生成，再按系统提示安装和信任。[Loon 证书工具](https://nsloon.app/certificate-tool/) · [Apple 证书信任说明](https://support.apple.com/zh-cn/102390)

**解密范围**　这个插件只声明 `mp.weixin.qq.com`、`app.bilibili.com`、`api.bilibili.com` 三个完整主机名。开启后 Loon 可以在设备上解密发往这三个主机的 HTTPS 流量，包括同主机的其他请求；只有四个指定接口会触发正文过滤。域名范围与其他已启用插件及主配置叠加。停用此插件可撤回它添加的规则和主机。[Loon MitM 说明](https://nsloon.app/docs/MitM/) · [原生复写文档](https://nsloon.app/docs/Rewrite/rewrite_v2/)

**实际验证**　刷新 B 站首页，确认推荐翻页和普通视频播放正常；打开原先含平台广告的公众号文章，确认阅读和互动正常。Loon 请求记录中的主机和路径可用来判断当前客户端是否走了这些接口。广告投放会轮换，一次没有广告不足以说明规则命中。接口改为其他路径或二进制格式时，覆盖范围会变化。视频画面中已经录入的口播、作者直接写入正文的推广及服务端拼接的视频贴片仍可能出现。这一版没有 iPad 真机命中率或速度降幅数据。

安装 Python 3，并将 jq 1.8.2 放入 PATH 后，在仓库根目录运行 `python -m unittest discover -s tests`，可执行整套离线回归测试。测试直接读取插件内的 URL 条件及 jq 表达式，覆盖正常条目、错误响应、相似路径、其他素材目录、大整数与重复执行。[抖音专项](tests/test_mobile.py) · [微博与酷安](tests/test_social.py) · [美团专项](tests/test_meituan.py) · [购物与常见 App](tests/test_suite.py) · [内嵌广告](tests/test_inline.py)

字段依据可对照 [B 站 App 与网页推荐处理](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/process/Response.mjs)、[B 站误拦记录](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/class/ADBlock.mjs#L123-L131)、[公众号独立广告入口](https://github.com/ihxperfect/loon-plugin/blob/54de749e8401b405883c16d1938d3385a70ee67f/startingad.plugin)和[公众号阅读互动响应示例](https://github.com/wnma3mz/wechat_articles_spider/blob/f8b31196e88045d079901812ea064ad4953d62a6/docs/%E4%BD%BF%E7%94%A8%E7%9A%84%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E6%8E%A5%E5%8F%A3.md#L161-L176)。

## 基础插件安装与验证

1. 在装有 Loon 的 iPhone 或 iPad 上用 Safari 打开上方安装链接，确认添加，并在 Loon 的「配置 → 插件」中启用「iPad 轻量去广告」。此链接跟随本仓库的 main 分支。
2. 如果安装链接没有唤起 Loon，在「配置 → 插件 → ＋」中粘贴[插件原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)。也可以把文件保存到「iCloud 云盘 → Loon → Plugins」，再在插件页填写完整文件名 `iPad-AdLite.lpx`。任选一种安装方式即可。
3. 在 Loon 运行并使用分流模式时，用 Safari 访问 `https://pagead2.googlesyndication.com/`。打开 Loon 请求记录，查看该主机命中的规则和拒绝策略。已有广告规则也可能拒绝它，单凭网页打不开无法确认是本插件命中。

## 基础插件覆盖范围

覆盖 Google 广告、百度广告、腾讯广告与腾讯音乐、字节与穿山甲、快手广告素材，以及微博和 WPS 的部分广告接口。插件只比较完整主机名，命中后交给 Loon 的 REJECT 策略处理。规则没有通配符、IP 段、远程脚本、远程子规则、DNS 指定或代理节点。

与正文或视频共用域名的广告，例如部分信息流和片中广告，仍可能显示。如果某个 App 等待广告才进入下一步，启动可能变慢，激励视频也可能无法领取奖励。遇到这种情况，可在插件页暂时关闭本插件并重试；对网速的实际影响取决于设备、已有规则和具体 App。

## 调研与规则依据

从六个公开来源逐项核查了 1,013 个插件、拆分模块及规则集链接，其中 759 份读到原文，可莉目录的 254 项在本次请求中返回 HTTP 403。逐项报告可下载后离线筛选。来自同一项目的拆分模块分别计数，数字不能用来推断使用人数或拦截率。[逐项核查报告](audit.html)

- Google 的移动广告调试文档和网页广告请求说明列出了广告服务主机。[AdMob](https://support.google.com/admob/answer/7671795) · [Ad Manager](https://support.google.com/admanager/answer/10358597?hl=en)
- 国内广告主机对照维护者的原始规则；各平台的主域和通用 CDN 均未作为后缀封锁。[AdGuard 移动广告规则](https://github.com/AdguardTeam/AdguardFilters/blob/master/MobileFilter/sections/adservers.txt) · [腾讯广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/tencent-ads) · [百度广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/baidu-ads) · [字节广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/bytedance-ads)
- 本插件采用 Loon 的精确域名和内置拒绝策略。[域名规则](https://nsloon.app/docs/Rule/domain_rule/) · [策略](https://nsloon.app/docs/Policy/) · [官方安装链接格式](https://nsloon.app/docs/Scheme/)
