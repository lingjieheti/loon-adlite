# 常用 App 去廣告（懶人版）

[简体中文](README.md) · **繁體中文** · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

我在 iPhone 和 iPad 上自用的外掛，分享給常用中國大陸 App 的朋友，包括在中國留學或工作的使用者。規則針對京東、淘寶、美團等 App 的部分開屏廣告，也能攔截網頁向已知廣告網域送出的請求。

## 安裝

**[一鍵安裝懶人版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [訂閱網址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

用 iPhone 或 iPad 的 Safari 開啟安裝連結，在 Loon 確認匯入。也可以將訂閱網址貼到 Loon 的「配置 → 外掛 → ＋」。網域攔截無需憑證，規則在裝置上執行，不載入遠端腳本，也不收集使用紀錄。

已訂閱「常用 App 去廣告」合併版的使用者，只需重新整理原訂閱。若先前使用本專案的其他去廣告外掛，請在啟用懶人版後停用舊項目，避免規則重複。

## 內嵌廣告

若要過濾微信公眾號文章、嗶哩嗶哩首頁等位置的部分廣告，請使用 Loon 3.5.1（978）或更新版本，開啟重寫，為列出的主機啟用 HTTPS 解密，並在裝置上信任自己產生的 Loon 憑證。同一主機的其他請求也可能被解密，處理回應會增加耗時。 [Loon 解密說明](https://nsloon.app/docs/MitM/)

抖音推薦頁規則已用樣本測試，目前 App 版本的實機效果仍待確認。已剪入影片的贊助片段需要手動跳過。

## Safari 選用功能

YouTube 網頁助手可在官方「略過廣告」按鈕出現時嘗試點擊。另有助手可隱藏 Pornhub 的部分廣告版位。 [安裝 YouTube 腳本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [安裝網頁腳本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

## 更新

GitHub 每天比對上游廣告網域，每次都執行安全稽核。已審核的網域清單有變動，且通過稽核與所有測試後，才會自動發佈到原訂閱網址。嗶哩嗶哩、京東等 App 的內嵌廣告規則來源也每天比對，需要調整的規則會先經過專項安全稽核。

訂閱網址跟隨 `main`。可將 Loon 的外部資源設為每天檢查更新。如需回到舊版，將訂閱網址的 `main` 改為該次提交的完整編號。 [提交紀錄](https://github.com/lingjieheti/loon-adlite/commits/main/)

[各 App 的涵蓋範圍（簡體中文）](COVERAGE.md) · [各功能的上游來源（簡體中文）](SOURCES.md) · [離線回歸測試](tests/) · [贊助這個專案（簡體中文）](SPONSOR.md) · [安全稽核](SECURITY-AUDIT.md)
