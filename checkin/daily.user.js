// ==UserScript==
// @name         京东与什么值得买 · 个人签到
// @namespace    https://github.com/lingjieheti/loon-adlite
// @version      1.0.1
// @updateURL    https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js
// @description  打开专用入口时，使用当前已登录页面的官方签到按钮。
// @match        https://www.smzdm.com/
// @match        https://bean.jd.com/myJingBean/list
// @run-at       document-idle
// @inject-into  content
// @noframes
// @grant        none
// ==/UserScript==

(() => {
    "use strict";

    if (window.top !== window.self) return;

    const jd = location.hostname === "bean.jd.com";
    const entry = jd ? "https://bean.jd.com/myJingBean/list#loon-checkin" : "https://www.smzdm.com/#loon-checkin";
    const attemptKey = jd ? "loon-adlite:jd:attempt-date" : "loon-adlite:smzdm:attempt-date";
    const jdSignImage = "https://img11.360buyimg.com/dl/jfs/t1/90191/32/54493/5536/6722f8bcF77a507b7/c5688a27a125651b.png";
    let timer;
    let frame;

    function onEntry() {
        return location.href === entry && document.visibilityState === "visible";
    }

    function beijingDate() {
        return new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString().slice(0, 10);
    }

    function visible(element) {
        if (!element || !element.getClientRects().length) return false;
        for (let node = element; node; node = node.parentElement) {
            const style = getComputedStyle(node);
            if (node.hidden || node.inert || node.getAttribute("aria-hidden") === "true" ||
                style.display === "none" || style.visibility !== "visible" || style.opacity === "0") return false;
        }
        return true;
    }

    function hasDialog() {
        return [...document.querySelectorAll('dialog[open], [role="dialog"], [aria-modal="true"]')].some(visible);
    }

    function only(scope, selector) {
        const matches = scope.querySelectorAll(selector);
        return matches.length === 1 ? matches[0] : null;
    }

    // A missing account/card can be the first, not-yet-hydrated render.
    // Return undefined to wait briefly, null to leave the decision to the user.
    function smzdmButton() {
        const header = only(document, "header.app-header");
        if (!header || !header.querySelector(".app-header__mine")) return undefined;
        if (header.querySelector(".app-header__guest, .header-checkin--done")) return null;
        const account = only(header, ".app-header__mine img.app-header__avatar");
        if (!account || !header.querySelector(".header-checkin button")) return undefined;
        const button = only(header, '.header-checkin button.header-checkin-button[type="button"]');
        if (!visible(account) || !visible(button) || button.disabled ||
            button.getAttribute("aria-disabled") === "true" || button.getAttribute("aria-busy") !== "false") return null;
        const label = only(button, 'span[aria-live="polite"]');
        if (!visible(label) || label.textContent.trim() !== "签到领奖") return null;
        return button;
    }

    function jdHasPendingDay(card) {
        const progress = only(card, ":scope > .progress");
        if (!visible(progress)) return false;
        const nodes = [...progress.querySelectorAll(":scope > .node, :scope > .reward_node")];
        const today = nodes.filter(node => {
            const label = only(node, ":scope > .text");
            return visible(label) && /^(今天|今天可领)$/.test(label.innerText.trim());
        });
        if (today.length !== 1 || today[0].classList.contains("sign-in")) return false;
        const previous = nodes[nodes.indexOf(today[0]) - 1];
        if (visible(previous) && previous.classList.contains("sign-in")) return true;
        const amount = only(today[0], ":scope > .txt_wrap > .txt_num");
        return today[0].classList.contains("reward_node") && visible(amount) && /^\+[1-9]\d*$/.test(amount.innerText.trim());
    }

    function jdButton() {
        const account = only(document, "#ttbar-login a.nickname");
        const card = only(document, "#bean-sign-component");
        if (!visible(account) || !visible(card)) return undefined;
        if ([...document.querySelectorAll("#ttbar-login .link-login")].some(visible)) return null;
        if ([...card.querySelectorAll(":scope > .mask, :scope > .guide")].some(visible)) return null;
        if (/请登录|去登录|验证码|安全验证|滑块验证|打开.{0,4}app|前往.{0,4}app|app.{0,5}(签到|领取)|支付|购买|抽奖/i.test(card.innerText)) return null;
        const title = only(card, ":scope > .header > .title");
        if (!title || !card.querySelector(":scope > .btn")) return undefined;
        if (!visible(title) || title.innerText.trim() !== "签到领京豆") return null;
        if (!jdHasPendingDay(card)) return undefined;

        const button = only(card, ":scope > .btn");
        if (!visible(button) || button.closest("a[href], form") || button.querySelector("a[href], button, input") ||
            button.hasAttribute("formaction") || button.hasAttribute("disabled") ||
            button.getAttribute("aria-disabled") === "true" || button.getAttribute("aria-busy") === "true") return null;
        const buttonImages = button.querySelectorAll("img");
        if (buttonImages.length > 1) return null;
        const image = buttonImages[0];
        const labels = [button.innerText, button.getAttribute("aria-label")];
        if (image) {
            if (!visible(image)) return null;
            labels.push(image.alt, image.getAttribute("aria-label"));
        }
        const names = labels.map(label => (label || "").trim()).filter(Boolean);
        if (names.length) return names.every(name => /^(签到领京豆|立即签到|签到)$/.test(name)) ? button : null;
        return image && image.parentElement === button && image.classList.contains("img") &&
            (image.currentSrc || image.src) === jdSignImage ? button : null;
    }

    function readyButton() {
        if (!onEntry() || hasDialog()) return null;
        return jd ? jdButton() : smzdmButton();
    }

    function center(button) {
        const rect = button.getBoundingClientRect();
        return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
    }

    function hit(button) {
        const { x, y } = center(button);
        const target = document.elementFromPoint(x, y);
        return target && button.contains(target);
    }

    function attempt(button) {
        const clickOnce = () => {
            const current = readyButton();
            if (current !== button || !hit(button)) return;
            const day = beijingDate();
            try {
                if (localStorage.getItem(attemptKey) === day) return;
                localStorage.setItem(attemptKey, day);
            } catch {
                return;
            }
            current.click();
        };
        // A second visible tab must not race the first tab to the same button.
        navigator.locks.request(attemptKey, { ifAvailable: true }, lock => {
            if (lock) clickOnce();
        }).catch(() => {});
    }

    function start() {
        clearTimeout(timer);
        cancelAnimationFrame(frame);
        if (!onEntry() || !navigator.locks) return;
        try {
            if (localStorage.getItem(attemptKey) === beijingDate()) return;
        } catch {
            return;
        }
        const until = Date.now() + 10000;
        let scrolled = false;
        function inspect() {
            const button = readyButton();
            if (!button) {
                if (button === undefined && Date.now() < until) timer = setTimeout(inspect, 400);
                return;
            }
            if (hit(button)) {
                attempt(button);
                return;
            }
            const { x, y } = center(button);
            if (!scrolled && (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight)) {
                scrolled = true;
                button.scrollIntoView({ block: "center", inline: "nearest", behavior: "instant" });
                frame = requestAnimationFrame(inspect);
            }
        }
        inspect();
    }

    window.addEventListener("hashchange", start);
    window.addEventListener("pagehide", () => { clearTimeout(timer); cancelAnimationFrame(frame); });
    document.addEventListener("visibilitychange", start);
    start();
})();
