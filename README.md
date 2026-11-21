# iPad 轻量去广告

用 22 条完整主机名规则拦截一部分网页和 App 广告。插件约 1.1 KiB，所有规则都在一个可直接阅读的文件里。使用 Loon 已有的分流功能即可，无需安装证书、启用 HTTPS 解密或执行脚本。

[在 iPad 上用 Loon 安装](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [查看插件原文](iPad-AdLite.lpx)

## 安装与验证

1. 在装有 Loon 的 iPad 上用 Safari 打开上方安装链接，确认添加，并在 Loon 的「配置 → 插件」中启用「iPad 轻量去广告」。此链接跟随本仓库的 main 分支。
2. 如果安装链接没有唤起 Loon，在「配置 → 插件 → ＋」中粘贴[插件原始地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)。也可以把文件保存到「iCloud 云盘 → Loon → Plugins」，再在插件页填写完整文件名 `iPad-AdLite.lpx`。任选一种安装方式即可。
3. 在 Loon 运行并使用分流模式时，用 Safari 访问 `https://pagead2.googlesyndication.com/`。打开 Loon 请求记录，查看该主机命中的规则和拒绝策略。已有广告规则也可能拒绝它，单凭网页打不开无法确认是本插件命中。

## 覆盖范围与使用取舍

覆盖 Google 广告、百度广告、腾讯广告与腾讯音乐、字节与穿山甲、快手广告素材，以及微博和 WPS 的部分广告接口。插件只比较完整主机名，命中后交给 Loon 的 REJECT 策略处理。规则没有通配符、IP 段、远程脚本、远程子规则、DNS 指定或代理节点。

与正文或视频共用域名的广告，例如部分信息流和片中广告，仍可能显示。如果某个 App 等待广告才进入下一步，启动可能变慢，激励视频也可能无法领取奖励。遇到这种情况，可在插件页暂时关闭本插件并重试；对网速的实际影响取决于设备、已有规则和具体 App。

## 调研与规则依据

从六个公开来源逐项核查了 1,013 个插件、拆分模块及规则集链接，其中 759 份读到原文，可莉目录的 254 项在本次请求中返回 HTTP 403。逐项报告可下载后离线筛选。来自同一项目的拆分模块分别计数，数字不能用来推断使用人数或拦截率。[逐项核查报告](audit.html)

- Google 的移动广告调试文档和网页广告请求说明列出了广告服务主机。[AdMob](https://support.google.com/admob/answer/7671795) · [Ad Manager](https://support.google.com/admanager/answer/10358597?hl=en)
- 国内广告主机对照维护者的原始规则；各平台的主域和通用 CDN 均未作为后缀封锁。[AdGuard 移动广告规则](https://github.com/AdguardTeam/AdguardFilters/blob/master/MobileFilter/sections/adservers.txt) · [腾讯广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/tencent-ads) · [百度广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/baidu-ads) · [字节广告域名](https://github.com/v2ray/domain-list-community/blob/master/data/bytedance-ads)
- 本插件采用 Loon 的精确域名和内置拒绝策略。[域名规则](https://nsloon.app/docs/Rule/domain_rule/) · [策略](https://nsloon.app/docs/Policy/) · [官方安装链接格式](https://nsloon.app/docs/Scheme/)
