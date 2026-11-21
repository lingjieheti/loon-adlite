# 我在 iPhone 和 iPad 上用的 Loon 廣告過濾規則

[简体中文](README.md) · **繁體中文** · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

我平常在中國大陸用京東和淘寶購物、用美團叫外送，就把自己在 Loon 裡用的規則整理在這裡。住在當地、來留學或工作，只要常用這些 App，都可以按需要選用。三個版本都在裝置上處理，不執行遠端腳本，也不收集使用紀錄。

## 選擇與安裝

第一次使用，建議從**輕量版**開始。在 iPhone 或 iPad 的 Safari 點選安裝連結，再到 Loon 確認匯入。也可以複製訂閱網址，在 Loon 的「配置 → 插件 → ＋」中貼上。

- **輕量版（Lite）** 會在完整主機名稱符合廣告清單時攔截連線，包括部分網頁的廣告競價請求。無需安裝憑證或開啟 HTTPS 解密。[安裝輕量版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [訂閱網址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **合併版（Suite）** 包含輕量版和內嵌版，另有京東、淘寶、美團及抖音等 App 的專用規則。選用後，請停用另外兩個版本。[安裝合併版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [訂閱網址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)
- **內嵌版（Inline）** 可搭配輕量版，過濾部分微信公眾號文章廣告、嗶哩嗶哩首頁的廣告卡片及部分開啟 App 時顯示的廣告。[安裝內嵌版](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [訂閱網址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)

合併版與內嵌版的改寫規則需要 Loon 3.5.1（組建版本 978）或更新版本。請開啟改寫功能，信任自己產生的 Loon 憑證，並為列出的主機啟用 HTTPS 解密。連到同一主機的其他請求也可能被解密。TLS 交握和回應處理都需要時間，實際影響取決於裝置和網路。[Loon 解密說明](https://nsloon.app/docs/MitM/)

## 影片與 Safari 小工具

抖音規則會辨認推薦動態中帶有廣告標記的項目，已用範例回應測試，目前版本的實機效果仍待確認。創作者剪進影片的贊助內容仍會播放。[各 App 的涵蓋範圍（簡體中文）](COVERAGE.md) · [各功能的上游來源（簡體中文）](SOURCES.md)

下列小工具需在 Safari 啟用 Userscripts 擴充功能後另行安裝。開啟腳本連結，從擴充功能選單安裝，允許在對應網站執行，再重新整理網頁。

- **YouTube 網頁版**可隱藏部分首頁和搜尋廣告位，並在官方「略過廣告」按鈕可用時嘗試點選。這個工具僅適用於 Safari 網頁版。[安裝 YouTube 腳本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Pornhub 網頁版**可隱藏部分側欄橫幅和行動版播放頁廣告位。與正片合併在同一條影音串流裡的廣告仍可能播放。[安裝網頁腳本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **簽到與領券**。可從同一頁前往京東領京豆、到「什麼值得買」每日簽到。在 Safari 開啟自己選定的京東一般優惠券或淘寶店舖券，可讓對應助手嘗試領取。淘寶紅包簽到、淘金幣及抖音活動請在官方頁面確認。[簽到與領券指南（簡體中文）](checkin/README.md)

## 更新與回復舊版

訂閱網址會跟隨 GitHub 的 `main` 分支更新。可將 Loon 設為每天檢查外部資源，實際更新時間由 Loon 決定。透過 USB 複製的本機檔案需自行替換。若要回復舊版，將訂閱網址中的 `main` 改為該次提交的完整雜湊值，匯入後停用原有項目。[提交紀錄](https://github.com/lingjieheti/loon-adlite/commits/main/)

[贊助這個專案（簡體中文）](SPONSOR.md)
