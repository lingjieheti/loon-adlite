# My all-in-one Loon ad filter

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · **English** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) | [Support my work](SPONSOR.en.md)

I use this plugin on my iPhone and iPad. It’s for anyone who uses mainland Chinese apps, including international students living in China. It targets some launch ads in JD, Taobao and Meituan, and blocks requests to known ad hosts on the web.

## Installation

**[Install the all-in-one plugin](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Open the install link in Safari and confirm the import in Loon, or paste the subscription URL under Configuration → Plugins → ＋. Hostname filtering works without a certificate. The plugin processes traffic on your device, loads no remote scripts and collects no usage data.

If you already subscribe to Suite, refresh your existing subscription. If you used another ad-blocking plugin from this project, disable its entry after enabling the all-in-one plugin to avoid duplicate rules.

## Ads embedded in apps

To filter certain ads in WeChat articles or the Bilibili home feed, use Loon 3.5.1 (build 978) or later. Enable rewrites and HTTPS decryption for the listed hosts, then trust your own Loon certificate on the device. Other requests to those hosts may also be decrypted. TLS handshakes and response processing add overhead. [Loon’s HTTPS decryption guide](https://nsloon.app/docs/MitM/)

The Douyin feed rules have been tested on sample responses. Their effect on the current app still needs checking on a device. Sponsor segments recorded as part of a video still play.

## Optional tools for Safari

The YouTube website helper tries to click the official Skip Ad button when it appears. A separate helper hides selected ad slots on Pornhub. [Install the YouTube userscript](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Install the Pornhub userscript](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js) · [Safari filtering options (Chinese)](web/README.md)

## Updates

GitHub checks the upstream ad host list daily and runs a security audit every time. It publishes changes to the approved host list at the same subscription URL only after the audit and all tests pass. It also checks upstream sources for in-app filters such as Bilibili and JD daily. Changes to those filters get a separate security review before release.

The subscription follows `main`. Set Loon to check external resources daily for automatic updates. To roll back, replace `main` in the subscription URL with the full commit hash you want. [Commit history](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Coverage and limitations by app (Chinese)](COVERAGE.md) · [Upstream sources by feature (Chinese)](SOURCES.md) · [Rule sources and review notes (Chinese)](audit.html) · [Offline regression tests](tests/) · [Security audit (Chinese)](SECURITY-AUDIT.md)
