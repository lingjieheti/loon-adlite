# My Loon ad filters for iPhone and iPad

[简体中文](README.md) · **English** · [日本語](README.ja.md) | [Support my work](SPONSOR.en.md)

I use these Loon plugins to filter ads that appear when an app opens or while I scroll through its feed. All three run on the device and use no remote scripts or telemetry. For the lowest overhead, start with Lite.

## Installation

For daily check-ins on JD and SMZDM, there is a separate Safari helper and an optional JD reminder for Loon. The helper runs when its dedicated page is open. [Check-in setup (Chinese)](checkin/README.md)

Open an install link in Safari on your iPhone or iPad, then confirm the import in Loon. You can also copy the subscription URL into Loon under Configuration → Plugins → ＋.

- **Suite** includes both Lite and Inline, plus rules for apps such as JD, Taobao, Meituan and Douyin. If you use Suite, disable the other two plugins to avoid applying the same rules twice. [Install Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **Lite** blocks requests to 39 specific hostnames that serve ads or ad assets. It uses the same hostname list as Suite and requires no HTTPS decryption or certificate. [Install Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** can be used alongside Lite to filter ads in WeChat Official Account articles, ad cards on the Bilibili home feed and some Bilibili launch ads. [Install Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [Subscription URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

Suite also targets posts marked as ads in Douyin’s recommendation feed. These rules have been tested with sample responses. Their effect on the current Douyin app still needs to be verified on a device. Sponsor segments recorded as part of a video still play.

## HTTPS decryption and performance

The rewrite rules in Suite and Inline require Loon 3.5.1 (build 978) or later. Enable rewrites and HTTPS decryption for the listed hostnames, and trust your own Loon certificate on the device. Loon can also decrypt other HTTPS requests to those same hosts. TLS handshakes and response processing add overhead that varies by device, network and app. [Loon’s HTTPS decryption guide](https://nsloon.app/docs/MitM/)

## Updates and rollback

Each subscription URL follows its edition on the `main` branch. GitHub checks the rules and privacy settings before changes are published. For automatic updates, set Loon to check external resources daily. Loon controls the actual refresh time. Files copied over USB need to be replaced manually.

To roll back, replace `main` in the subscription URL with the full commit hash of the version you want. Import that URL and disable the previous entry. [Commit history](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Coverage and limitations by app (Chinese)](COVERAGE.md) · [Rule sources and review notes (Chinese)](audit.html) · [Offline regression tests](tests/)
