// ==UserScript==
// @name         YouTube 网页广告助手
// @namespace    https://github.com/lingjieheti/loon-adlite
// @version      1.0.0
// @description  收起列表中的独立广告位，并在播放器允许跳过时尝试点击一次。
// @match        https://www.youtube.com/*
// @match        https://m.youtube.com/*
// @noframes
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(() => {
    "use strict";
    if (window.top !== window.self ||
        !["https://www.youtube.com", "https://m.youtube.com"].includes(location.origin)) return;

    const listRules = {
        "/": "#contents > ytd-rich-item-renderer > ytd-ad-slot-renderer, ytd-rich-item-renderer > #content > ytd-ad-slot-renderer, ytm-rich-item-renderer > ad-slot-renderer",
        "/results": "ytd-item-section-renderer > .ytd-item-section-renderer > ytd-ad-slot-renderer, lazy-list > ad-slot-renderer",
    };
    const skipSelector = [
        ".ytp-ad-module button.ytp-ad-skip-button",
        ".ytp-ad-module button.ytp-ad-skip-button-modern",
        ".ytp-ad-module button.ytp-skip-ad-button",
        ".ytp-skip-ad > button.ytp-skip-ad-button",
    ].join(", ");
    const listStyle = document.createElement("style");
    let player = null;
    let lastButton = null;
    let videoId = null;
    let observingAd = false;
    let searching = false;
    let searchTimeout;
    let frame = 0;

    function watchId() {
        if (location.pathname !== "/watch") return null;
        return new URLSearchParams(location.search).get("v") || null;
    }

    function actionable(button) {
        if (button.matches(":disabled") || button.closest('[hidden], [inert], [aria-hidden="true"], [aria-disabled="true"], a[href]')) return false;
        const rect = button.getBoundingClientRect();
        if (!rect.width || !rect.height || getComputedStyle(button).pointerEvents === "none") return false;
        // Countdown labels can occupy the same control before the skip action is enabled.
        if (/\p{Nd}/u.test(button.innerText + (button.getAttribute("aria-label") || ""))) return false;
        for (let el = button; el; el = el.parentElement) {
            const style = getComputedStyle(el);
            if (style.visibility !== "visible" || style.opacity === "0") return false;
        }
        return true;
    }

    function checkButton() {
        frame = 0;
        if (document.hidden || !player?.isConnected || !videoId || watchId() !== videoId ||
            !player.classList.contains("ad-showing")) return;
        const ready = [...player.querySelectorAll(skipSelector)].filter(actionable);
        if (!ready.length) lastButton = null;
        if (ready.length !== 1 || ready[0] === lastButton) return;
        const button = ready[0];
        const rect = button.getBoundingClientRect();
        const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
        if (!hit || !button.contains(hit)) return;
        lastButton = button;
        button.click();
    }

    function queueCheck() {
        if (!frame && observingAd) frame = requestAnimationFrame(checkButton);
    }

    const controls = new MutationObserver(queueCheck);
    function syncAd() {
        const active = Boolean(player?.classList.contains("ad-showing"));
        if (!active) lastButton = null;
        if (active !== observingAd) {
            controls.disconnect();
            observingAd = active;
            if (active) controls.observe(player, {
                subtree: true, childList: true, characterData: true, attributes: true,
                attributeFilter: ["class", "style", "hidden", "disabled", "inert", "aria-disabled", "aria-hidden", "aria-label"],
            });
        }
        queueCheck();
    }

    const adState = new MutationObserver(syncAd);
    const mount = new MutationObserver(findPlayer);
    function stopSearch() {
        clearTimeout(searchTimeout);
        mount.disconnect();
        searching = false;
    }

    function unbind() {
        stopSearch();
        controls.disconnect();
        adState.disconnect();
        cancelAnimationFrame(frame);
        frame = 0;
        observingAd = false;
        player = null;
    }

    function findPlayer() {
        if (document.hidden || !videoId || watchId() !== videoId) return;
        if (player?.isConnected) return;
        // The mobile page can mount its player without the desktop movie_player id.
        const players = document.querySelectorAll(".html5-video-player");
        if (players.length !== 1) {
            if (!searching) {
                mount.observe(document.body, { subtree: true, childList: true });
                searching = true;
                searchTimeout = setTimeout(stopSearch, 10000);
            }
            return;
        }
        unbind();
        player = players[0];
        adState.observe(player, { attributes: true, attributeFilter: ["class"] });
        syncAd();
    }

    function syncPage() {
        const selectors = listRules[location.pathname];
        if (selectors) {
            const css = selectors + " { display: none !important; }";
            if (listStyle.textContent !== css) listStyle.textContent = css;
            if (!listStyle.isConnected) document.head.append(listStyle);
        } else {
            listStyle.remove();
        }
        const current = watchId();
        if (current !== videoId) lastButton = null;
        if (current !== videoId || document.hidden) unbind();
        videoId = current;
        findPlayer();
    }

    document.addEventListener("yt-navigate-finish", syncPage);
    document.addEventListener("yt-page-data-updated", syncPage);
    document.addEventListener("state-navigateend", syncPage);
    document.addEventListener("visibilitychange", syncPage);
    // Player replacement and mobile navigation may finish after the route event.
    document.addEventListener("playing", syncPage, true);
    window.addEventListener("pageshow", syncPage);
    window.addEventListener("popstate", syncPage);
    window.addEventListener("pagehide", unbind);
    window.addEventListener("resize", queueCheck);
    syncPage();
})();
