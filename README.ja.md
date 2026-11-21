# iPhone・iPad 向けの軽量広告フィルター（Loon 用）

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · **日本語** · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) ｜ [開発を応援する](SPONSOR.ja.md)

中国のアプリを日常的に使う方や中国に留学中の方向けに、私が iPhone と iPad で使っている購読を公開しています。購読は一つで、京東・淘宝・美団などのアプリやウェブからの通信は、ホスト名がリスト内の広告ドメインと完全に一致したときに端末上で遮断します。アプリ内の一部の広告には、特定のリクエストにだけ適用する書き換えルールも任意で有効にできます。

## インストール

**[オールインワン版をインストール](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [購読用 URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

iPhone または iPad の Safari でリンクを開き、Loon で読み込みを承認します。購読用 URL を「設定 → プラグイン → ＋」に貼り付けることもできます。ドメイン単位のブロックに証明書は不要です。処理は端末内で完結し、外部スクリプトの読み込みや利用記録の収集はありません。

従来の統合版（Suite）を購読中の方は、その購読を更新するだけで使えます。このプロジェクトの別の広告ブロック用プラグインを使っていた方は、ルールが重複しないよう、オールインワン版を有効にした後で以前の項目を無効にしてください。

## アプリ内の広告

WeChat 公式アカウントの記事や Bilibili のホームにある一部の広告を除くには、Loon 3.5.1（ビルド 978）以降で書き換えと対象ホストの HTTPS 復号を有効にし、自分で生成した Loon 証明書を端末で信頼します。同じホストへのほかの通信も復号される場合があり、TLS 接続や応答処理に時間がかかります。 [Loon の HTTPS 復号について](https://nsloon.app/docs/MitM/)

抖音のおすすめフィード用ルールはサンプルで確認済みです。現行アプリでの実機検証は済んでいません。動画に収録されたスポンサー紹介は手動でスキップしてください。

## Safari の追加機能

YouTube ウェブ版の補助スクリプトは、公式の「広告をスキップ」ボタンが表示されるとクリックを試みます。Pornhub の一部の広告枠を隠すスクリプトもあります。 [YouTube 用スクリプトを開く](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Pornhub 用スクリプトを開く](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

## 更新

GitHub は毎日、広告ホストを上流の一覧と照合し、その都度セキュリティ監査を行います。承認済みホストの一覧に変更があり、監査とすべてのテストを通過した場合に、同じ購読 URL に自動公開します。Bilibili や京東のアプリ内広告ルールについても参照元を毎日確認し、ルールを変更する場合は公開前に個別のセキュリティ審査を行います。

購読先は `main` です。Loon の外部リソースを毎日更新確認する設定にできます。以前の版に戻すには、購読用 URL の `main` を対象コミットの完全なハッシュ値に置き換えてください。 [コミット履歴](https://github.com/lingjieheti/loon-adlite/commits/main/)

[アプリ別の対応範囲と制限（簡体字中国語）](COVERAGE.md) · [機能別の参照元（簡体字中国語）](SOURCES.md) · [ルールの出典と検証記録（簡体字中国語）](audit.html) · [オフライン回帰テスト](tests/) · [セキュリティ監査（中国語）](SECURITY-AUDIT.md)
