# 个人自用的 Loon 去广告

**简体中文** · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) ｜ [赞助我](SPONSOR.md)

这是我自己在 iPhone 和 iPad 上用的 Loon 去广告插件，分享给常用中国大陆 App 的朋友，包括中国用户、在华留学生，以及来华工作或生活的朋友。平时用京东、淘宝购物，用美团点外卖，都能用上这套规则。

插件可过滤部分开屏和信息流广告，覆盖范围因 App 而异。第一次用 Loon，建议从轻量版开始，无需安装证书。三个去广告版本都在本机处理，不加载远程脚本，也不收集使用数据。

合并版可过滤哔哩哔哩首页中带广告标记的推荐。抖音规则也针对带标记的推荐流广告，当前版本的实机效果仍待验证。已经剪进视频的口播或赞助片段需要手动跳过。

在 Safari 看 YouTube，可以单独安装网页助手，收起部分首页和搜索广告，并在官方「跳过广告」按钮可用时尝试自动点击。YouTube 原生 App 不在此助手的覆盖范围内。[安装 YouTube 网页助手](youtube/README.md)

轻量版和合并版也能拦截部分普通网页广告请求，包括 PubMatic、Criteo 的广告竞价，以及 Pornhub 使用的部分广告服务。在 iPad 的 Safari 里，还可以按需隐藏 Pornhub 侧栏横幅和移动播放页广告位。想过滤更多网站上的横幅和广告位，可在 Safari 单独启用 AdGuard。[网页过滤与 Safari 设置](web/README.md)

签到领券入口集中在一页。京东可签京豆，什么值得买可每日签到；在 Safari 打开指定京东普通券页面，还可选择让助手尝试领取。淘宝和抖音的签到或领券活动，在各自官方活动页或 App 内确认。[打开签到与领券指南](checkin/README.md)

## 安装

用 iPhone 或 iPad 的 Safari 点安装链接，在 Loon 确认导入，也可以在「配置 → 插件 → ＋」粘贴对应的订阅地址。

- **合并版**｜包含轻量版和内嵌版，另有购物、外卖、社交等 App 的定向规则。使用合并版时，停用另外两个版本即可。[安装合并版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **轻量版**｜与合并版共用广告主机清单，只拦截完整主机名与清单条目一致的请求，无需 HTTPS 解密或安装证书。[安装轻量版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)

## 内嵌广告插件

只想在轻量版上加微信公众号文章广告、哔哩哔哩首页和部分开屏过滤时，可单独加装内嵌版。[安装内嵌版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

合并版和内嵌版的复写需要 Loon 3.5.1（978）或更新版本，并在设备上开启复写、为指定主机启用 HTTPS 解密、信任自己的 Loon 证书。同主机上的其他请求也可能经过解密。TLS 握手和解析响应会消耗时间，实际开销随设备、网络和 App 而变。[Loon 解密说明](https://nsloon.app/docs/MitM/)

## 更新与回退

上方订阅地址始终指向同一版本线。GitHub 自动检查规则和隐私权限，测试通过后才发布到 `main`。建议让 Loon 的外部资源每天自动检查一次，实际刷新时间由客户端决定。通过 USB 复制的本地文件需手动替换。

需要回退时，可把订阅地址中的 `main` 换成某次提交的完整编号，导入后停用原条目。[提交历史](https://github.com/lingjieheti/loon-adlite/commits/main/)

[按 App 查看覆盖与限制](COVERAGE.md) · [规则来源核查报告](audit.html) · [离线回归测试](tests/)
