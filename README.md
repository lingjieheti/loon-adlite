# iPad 轻量去广告

## 常用 App 合并版

**[在 iPad 上安装常用 App 合并版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [插件原文](iPad-AdSuite.lpx) · [逐项覆盖与依据](COVERAGE.md)

这一个文件已包含下面两个旧版的规则，同时增加京东、淘宝、拼多多、闲鱼、菜鸟，以及多款生活和影音 App 的广告处理。购物场景针对已识别的广告素材、开屏配置和部分首页推广楼层。小红书、知乎、B 站和微信公众号另有内嵌广告规则。39 条精确域名规则和 15 条原生复写均内置，无远程脚本。

1. 用 iPad 上的 Safari 打开安装链接，在 Loon 确认添加并启用「iPad 常用 App 去广告」。若链接无法唤起 Loon，可在「配置 → 插件 → ＋」粘贴[原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)。
2. 如果装过「iPad 轻量去广告」或「iPad 内嵌广告过滤」，请在合并版启用后关闭这两个旧插件，避免重复匹配。回退时关闭合并版，再打开原来使用的版本即可。
3. 域名规则在 Loon 分流模式下工作。首页和开屏接口复写需要 Loon 3.5.1 (978) 或更新版、开启复写与 HTTPS 解密，并在设备上信任自己的 Loon CA。如果已经配置过，可沿用现有证书。合并版为 15 个完整主机声明解密，包括京东和淘宝的共享 API 主机；同一主机的其他 HTTPS 流量也可能由 Loon 在设备上解密，具体复写只匹配列出的路径。没有 CA 时仍可使用域名部分。[Loon 说明](https://nsloon.app/docs/MitM/) · [Apple 证书信任设置](https://support.apple.com/zh-cn/102390)

启用后，可打开淘宝首页、京东首页，再查看一件商品及购物车，检查开屏、图片、价格和优惠券是否正常。规则按已知接口编写，当前客户端可能改用新协议，也可能使用缓存素材。遇到白屏、商品图缺失或等待变长，可先停用合并版并重复相同步骤，比较差异。

## 基础版和内嵌版

基础插件按 22 个完整主机名拦截广告请求，约 1.1 KiB。另有一个可选的内嵌广告插件，针对与正常内容一起下发的广告，使用 Loon 原生 JSON 复写。两者可一起使用，均不加载远程脚本。

[安装基础插件](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [安装内嵌广告插件](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [基础插件原文](iPad-AdLite.lpx) · [内嵌插件原文](iPad-InlineAds.lpx)

## 内嵌广告插件

| 使用场景 | 处理内容 | 保留内容 |
| --- | --- | --- |
| 微信公众号文章 | 清空广告接口或阅读互动接口返回的广告列表，并把对应计数归零 | 正文、阅读数、点赞和其他互动字段 |
| 哔哩哔哩 App 首页 | 根据卡片类型和跳转类型共同识别广告卡，移除混排横幅中标记为广告的子项 | 普通视频、直播、活动横幅和未知卡片，保持原顺序 |
| 哔哩哔哩网页首页 | 移除推荐列表中明确标注为广告的卡片 | 带广告位元数据的普通视频和分页信息 |

在 iPad 上用 Safari 点「安装内嵌广告插件」，确认导入并启用「iPad 内嵌广告过滤」。已有基础版可以继续使用。若链接未唤起 Loon，可在「配置 → 插件 → ＋」粘贴[内嵌插件原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)。

**使用条件**　Loon 3.5.1 (978) 或更新版，已开启复写和 HTTPS 解密，并在 iPad 上信任自己的 Loon CA。如果设备还没有 CA，可使用 Loon 官方证书工具在本机生成，再按系统提示安装和信任。[Loon 证书工具](https://nsloon.app/certificate-tool/) · [Apple 证书信任说明](https://support.apple.com/zh-cn/102390)

**解密范围**　这个插件只声明 `mp.weixin.qq.com`、`app.bilibili.com`、`api.bilibili.com` 三个完整主机名。开启后 Loon 可以在设备上解密发往这三个主机的 HTTPS 流量，包括同主机的其他请求；只有四个指定接口会触发正文过滤。域名范围与其他已启用插件及主配置叠加。停用此插件可撤回它添加的规则和主机。[Loon MitM 说明](https://nsloon.app/docs/MitM/) · [原生复写文档](https://nsloon.app/docs/Rewrite/rewrite_v2/)

**实际验证**　刷新 B 站首页，确认推荐翻页和普通视频播放正常；打开原先含平台广告的公众号文章，确认阅读和互动正常。Loon 请求记录中的主机和路径可用来判断当前客户端是否走了这些接口。广告投放会轮换，一次没有广告不足以说明规则命中。接口改为其他路径或二进制格式时，覆盖范围会变化。视频画面中已经录入的口播、作者直接写入正文的推广及服务端拼接的视频贴片仍可能出现。这一版没有 iPad 真机命中率或速度降幅数据。

本地回归直接从插件读取 URL 匹配条件及 jq 表达式，覆盖正常条目、错误响应、未知字段、大整数和重复执行。使用 Python 3 并将 jq 1.8.2 放入 PATH 后，在仓库根目录运行 `python tests/test_inline.py`。这些测试使用离线样例。[回归测试](tests/test_inline.py)

字段依据可对照 [B 站 App 与网页推荐处理](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/process/Response.mjs)、[B 站误拦记录](https://github.com/Biliverse/ADBlock/blob/b0051916843f269d4b377aaf177f0d9e7b12e393/src/class/ADBlock.mjs#L123-L131)、[公众号独立广告入口](https://github.com/ihxperfect/loon-plugin/blob/54de749e8401b405883c16d1938d3385a70ee67f/startingad.plugin)和[公众号阅读互动响应示例](https://github.com/wnma3mz/wechat_articles_spider/blob/f8b31196e88045d079901812ea064ad4953d62a6/docs/%E4%BD%BF%E7%94%A8%E7%9A%84%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E6%8E%A5%E5%8F%A3.md#L161-L176)。

## 基础插件安装与验证

1. 在装有 Loon 的 iPad 上用 Safari 打开上方安装链接，确认添加，并在 Loon 的「配置 → 插件」中启用「iPad 轻量去广告」。此链接跟随本仓库的 main 分支。
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
