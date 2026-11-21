# 常用 App 去广告（懒人版）

**简体中文** · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) ｜ [赞助我](SPONSOR.md)

我在 iPhone 和 iPad 上自用的插件，分享给日常使用中国大陆 App 的朋友，包括在华留学生。规则针对京东、淘宝、美团等常用 App 的部分开屏广告，也能拦截网页向已知广告域名发出的请求。

## 安装

**[一键安装懒人版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

在 iPhone 或 iPad 上用 Safari 打开安装链接，在 Loon 确认导入。也可以把订阅地址粘贴到 Loon 的「配置 → 插件 → ＋」。域名拦截无需证书，规则在设备上运行，不加载远程脚本，也不收集使用记录。

已订阅「常用 App 去广告」合并版的用户，刷新原订阅即可。用过本项目其他去广告插件的用户，请在启用懒人版后停用旧的去广告条目，避免规则重复。

## 内嵌广告

需要过滤微信公众号文章、哔哩哔哩首页等位置的部分广告时，请在 Loon 3.5.1（978）或更新版本中开启复写，为插件列出的主机启用 HTTPS 解密，并在设备上信任自己生成的 Loon 证书。同一主机的其他请求也可能被解密，握手和处理响应会增加开销。 [Loon 解密说明](https://nsloon.app/docs/MitM/)

抖音推荐流规则通过了样本测试，当前 App 版本的实机效果仍待验证。已经剪进视频的口播广告需要手动跳过。

## 可选的 Safari 功能

YouTube 网页助手可在官方「跳过广告」按钮出现时尝试点击。网页过滤指南另有隐藏 Pornhub 部分广告位的助手。 [安装 YouTube 网页助手](youtube/README.md) · [网页过滤与 Safari 设置](web/README.md)

可以签到领京豆，也可以在什么值得买每日签到。在 Safari 打开自己选中的京东普通券或淘宝店铺券，助手会尝试领券。抖音活动仍需在官方页面操作。 [打开签到与领券指南](checkin/README.md)

## 更新

GitHub 每周核对一组已审核的广告域名，清单有变化且测试通过时，自动发布到同一个订阅地址。哔哩哔哩、京东等 App 的内嵌广告规则单独审核。 [自动更新记录](https://github.com/lingjieheti/loon-adlite/actions/workflows/sync-ad-hosts.yml)

订阅地址跟随 `main`。在 Loon 把外部资源设为每天检查，即可随客户端刷新获取新版。回退时可把订阅地址中的 `main` 替换为目标提交的完整编号。 [提交历史](https://github.com/lingjieheti/loon-adlite/commits/main/) · [上游变动报告](https://github.com/lingjieheti/loon-adlite/actions/workflows/review-upstreams.yml)

[按 App 查看覆盖与限制](COVERAGE.md) · [逐项查看上游来源与适配](SOURCES.md) · [规则来源核查报告](audit.html) · [离线回归测试](tests/) · [安全审计](SECURITY-AUDIT.md)
