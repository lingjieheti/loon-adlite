# iPhone・iPad 用の Loon 広告ブロック

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · **日本語** · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md) ｜ [開発を応援する](SPONSOR.ja.md)

自分の iPhone と iPad で使うために作った Loon プラグインです。中国本土のアプリを普段から使う方や、留学や仕事で中国に暮らす方に向けて公開しています。買い物で使う京東（JD）や淘宝（Taobao）、出前を頼むときの美団（Meituan）などが対象です。

アプリに応じて、起動時やフィードに表示される広告の一部をブロックします。Loon が初めての方には、証明書のインストールが不要な軽量版がおすすめです。3 つの版はいずれも端末内で処理し、外部スクリプトの実行や利用データの収集は行いません。

## インストール

Safari で YouTube を見る場合は、ホームや検索結果の一部の広告枠を隠し、スキップできるようになったら公式ボタンを押す専用スクリプトも使えます。対象はブラウザ版です。Safari で Userscripts を有効にし、次のリンクを開いて拡張機能のメニューからインストールしてください。[YouTube 用スクリプトを開く](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)

軽量版と統合版は、PubMatic や Criteo の広告入札用ホスト、Pornhub で使われる一部の広告配信先への通信もブロックします。Safari では、専用スクリプトで Pornhub のサイドバーやモバイル再生ページの一部の広告枠を非表示にできます。Userscripts からインストールし、対象サイトでの実行を許可してページを再読み込みしてください。動画に組み込まれた広告は再生されることがあります。[Pornhub 用スクリプトを開く](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

京東と「什么值得买」のチェックインには、対象ページを Safari で開いたときに動く専用スクリプトがあります。Loon の京東リマインダーも任意で追加できます。[設定方法（中国語）](checkin/README.md)

iPhone または iPad の Safari でインストールリンクを開き、Loon で読み込みを確定します。購読 URL をコピーして、Loon のプラグイン一覧の「＋」から追加することもできます。

- **統合版**は、軽量版とインライン広告版の全ルールに、京東・淘宝・美団などのアプリ向けルールを加えたものです。統合版を使う場合は、ほかの 2 つを無効にしてください。[統合版をインストール](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [購読 URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **軽量版**は、通信処理の負荷を抑えたい方向けです。接続先のホスト名が広告リストの項目と完全に一致した場合にブロックします。このリストは統合版と共通です。HTTPS の復号や証明書のインストールは不要です。[軽量版をインストール](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [購読 URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)

## インライン広告版

軽量版に、WeChat 公式アカウントの記事広告や、bilibili のホーム画面と起動時の一部広告のフィルタリングを追加したい場合に使います。[インライン広告版をインストール](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [購読 URL](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

統合版には、抖音（Douyin）のおすすめフィードで広告と明示された投稿を取り除くルールもあります。サンプルデータで動作を確認していますが、現行の抖音アプリでの効果は実機での確認が必要です。bilibili や抖音の動画本編に収録された商品紹介やスポンサー告知は手動でスキップしてください。

統合版とインライン広告版の書き換え機能には、Loon 3.5.1（ビルド 978）以降が必要です。端末で書き換えを有効にし、対象ホストの HTTPS 復号を有効にしたうえで、自分の Loon 証明書を信頼するよう設定してください。同じホスト宛てのほかの通信も復号される場合があります。TLS ハンドシェイクや応答の解析にかかる時間は、端末、回線、アプリによって異なります。[Loon の HTTPS 復号について](https://nsloon.app/docs/MitM/)

## 更新と以前の版への戻し方

上記の購読 URL で、選んだ版の更新を受け取れます。GitHub でルールとプライバシーに関わる権限のチェックを通過した変更が `main` に公開されます。Loon の外部リソースは 1 日 1 回の自動更新確認を推奨します。実際の更新時刻は Loon が決めます。USB 経由でコピーしたファイルは手動で差し替えてください。

以前の版に戻すには、購読 URL の `main` を使いたいコミットの完全なハッシュ値に置き換えます。その URL を Loon に追加したら、元の項目を無効にしてください。[コミット履歴](https://github.com/lingjieheti/loon-adlite/commits/main/)

[アプリ別の対応範囲と制限（簡体字中国語）](COVERAGE.md) · [ルールの出典と検証記録（簡体字中国語）](audit.html) · [オフライン回帰テスト](tests/)
