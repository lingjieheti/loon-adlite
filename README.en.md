# My Loon ad filters for iPhone and iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · **English** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) | [Support my work](SPONSOR.en.md)

These are the Loon filters I use on my own iPhone and iPad. They’re for anyone who uses mainland Chinese apps in daily life, from local users to international students and others living or working in China. They cover apps like JD (京东) and Taobao (淘宝) for shopping, and Meituan (美团) for food delivery.

The filters block some ads at launch or in feeds, depending on the app. If you’re new to Loon, start with Lite. It requires no certificate. All three editions filter traffic on your device, run no remote scripts and collect no usage data.

## Installation

For YouTube in Safari, an optional userscript hides some ad slots on the home and search pages and tries to click the player’s Skip Ad button when it becomes available. It runs only on the website. In Safari with Userscripts enabled, open the script and choose Install from the extension menu. [Install the YouTube userscript](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)

Lite and Suite also block requests to selected web ad hosts, including PubMatic and Criteo auction endpoints and ad services used on Pornhub. An optional Safari script hides identifiable Pornhub sidebar banners and mobile ad slots. Open the script in Safari, install it from the Userscripts extension, then allow it on that site and reload. Ads stitched into the video can still play. For banners and ad slots across more websites, you can enable AdGuard in Safari. [Safari filtering options (Chinese)](web/README.md) · [Install the Pornhub userscript](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

The rewards guide brings together JD Beans and SMZDM daily check-ins with coupon links for JD, Taobao and Douyin. In Safari, an optional helper can try to claim a standard JD coupon or a Taobao shop coupon you select. Use the official promotion page or app for Taobao check-ins and Douyin offers. [Check-in and coupon guide (Chinese)](checkin/README.md)

Open an install link in Safari on your iPhone or iPad, then confirm the import in Loon. You can also copy the subscription URL into Loon under Configuration → Plugins → ＋.

- **Suite** includes both Lite and Inline, plus rules for apps such as JD, Taobao, Meituan and Douyin. If you use Suite, disable the other two plugins to avoid applying the same rules twice. [Install Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **Lite** blocks a request when its hostname exactly matches an entry on the ad list. It uses the same hostname list as Suite and requires no HTTPS decryption or certificate. [Install Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** can be used alongside Lite to filter ads in WeChat Official Account articles, ad cards on the Bilibili home feed and some Bilibili launch ads. [Install Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

Suite also targets posts marked as ads in Douyin’s recommendation feed. These rules have been tested with sample responses. Their effect on the current Douyin app still needs to be verified on a device. Sponsor segments recorded as part of a video still play.

## HTTPS decryption and performance

The rewrite rules in Suite and Inline require Loon 3.5.1 (build 978) or later. Enable rewrites and HTTPS decryption for the listed hostnames, and trust your own Loon certificate on the device. Loon can also decrypt other HTTPS requests to those same hosts. TLS handshakes and response processing add overhead that varies by device, network and app. [Loon’s HTTPS decryption guide](https://nsloon.app/docs/MitM/)

## Updates and rollback

Each subscription URL follows its edition on the `main` branch. GitHub checks the rules and privacy settings before changes are published. For automatic updates, set Loon to check external resources daily. Loon controls the actual refresh time. Files copied over USB need to be replaced manually.

To roll back, replace `main` in the subscription URL with the full commit hash of the version you want. Import that URL and disable the previous entry. [Commit history](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Coverage and limitations by app (Chinese)](COVERAGE.md) · [Rule sources and review notes (Chinese)](audit.html) · [Offline regression tests](tests/)
