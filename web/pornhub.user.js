// ==UserScript==
// @name         Pornhub 网页广告位过滤
// @namespace    https://github.com/lingjieheti/loon-adlite
// @version      1.0.0
// @updateURL    https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js
// @description  在本站隐藏部分侧栏横幅、移动播放页广告位和独立广告投放元素。
// @match        https://*.pornhub.com/*
// @noframes
// @inject-into  content
// @run-at       document-end
// @grant        none
// ==/UserScript==

(() => {
    "use strict";
    const host = location.hostname;
    if (window.top !== window.self || location.protocol !== "https:" ||
        (host !== "pornhub.com" && !host.endsWith(".pornhub.com"))) return;
    if (!document.head || document.getElementById("loon-adlite-ph-ad-slots")) return;

    const style = document.createElement("style");
    style.id = "loon-adlite-ph-ad-slots";
    style.textContent = `
        .sideAds,
        #mobileContainer .watchpageAd,
        ins.adsbytrafficjunky,
        a[href^="https://ads.trafficjunky.net/"] {
            display: none !important;
        }
    `;
    document.head.append(style);
})();
