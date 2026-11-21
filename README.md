# 个人自用的 Loon 去广告

给自己的 iPhone 和 iPad 用，主要过滤常用 App 的开屏和信息流广告。优先考虑低开销的用户可以从轻量版开始。三个版本都在本机处理，没有远程脚本或遥测。

## 安装

用 iPhone 或 iPad 的 Safari 点安装链接，在 Loon 确认导入，也可以在「配置 → 插件 → ＋」粘贴对应的订阅地址。

- **合并版**｜包含轻量版和内嵌版，另有购物、外卖、社交等 App 的定向规则。使用合并版时，停用另外两个版本即可。[安装合并版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **轻量版**｜与合并版共用 39 个完整广告域名，适合只拦广告投送和素材请求的设备，无需 HTTPS 解密或安装证书。[安装轻量版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)

## 内嵌广告插件

只想在轻量版上加微信公众号文章广告、哔哩哔哩首页和部分开屏过滤时，可单独加装内嵌版。[安装内嵌版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

合并版和内嵌版的复写需要 Loon 3.5.1（978）或更新版本，并在设备上开启复写、为指定主机启用 HTTPS 解密、信任自己的 Loon 证书。同主机上的其他请求也可能经过解密。TLS 握手和解析响应会消耗时间，实际开销随设备、网络和 App 而变。[Loon 解密说明](https://nsloon.app/docs/MitM/)

## 更新与回退

上方订阅地址始终指向同一版本线。GitHub 自动检查规则和隐私权限，测试通过后才发布到 `main`。建议让 Loon 的外部资源每天自动检查一次，实际刷新时间由客户端决定。通过 USB 复制的本地文件需手动替换。

需要回退时，可把订阅地址中的 `main` 换成某次提交的完整编号，导入后停用原条目。[提交历史](https://github.com/lingjieheti/loon-adlite/commits/main/)

[按 App 查看覆盖与限制](COVERAGE.md) · [规则来源核查报告](audit.html) · [离线回归测试](tests/)
