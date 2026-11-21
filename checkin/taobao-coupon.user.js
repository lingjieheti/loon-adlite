// ==UserScript==
// @name         淘宝 · 领取我选的一张店铺券
// @namespace    https://github.com/lingjieheti/loon-adlite
// @version      1.0.0
// @updateURL    https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/taobao-coupon.user.js
// @description  在选定的淘宝普通店铺券页面，尝试点击一次「确认领取」。
// @match        https://market.m.taobao.com/apps/aliyx/coupon/detail.html*
// @run-at       document-idle
// @inject-into  content
// @noframes
// @grant        none
// ==/UserScript==

(() => {
    "use strict";

    const base = "https://market.m.taobao.com/apps/aliyx/coupon/detail.html";
    const query = location.search;
    // Taobao's page reads the full URL. The final ampersand separates its last ID from the opt-in fragment.
    if (window.self !== window.top || location.href.split("#")[0] !== base + query ||
        !query.endsWith("&")) return;
    const fields = query.slice(0, -1);
    if (!/^\?[A-Za-z_]+=[A-Za-z0-9]+(?:&[A-Za-z_]+=[A-Za-z0-9]+){2}$/.test(fields)) return;
    const params = new URLSearchParams(fields);
    if ([...params].length !== 3 || params.get("wh_weex") !== "true") return;
    const seller = params.get("sellerId"), activity = params.get("activityId");
    if (!/^[1-9][0-9]{0,19}$/.test(seller || "") || !/^[\da-f]{32}$/i.test(activity || "")) return;

    const entry = base + query + "#loon-coupon=" + seller + "." + activity;
    const storageKey = "loon-adlite:taobao:coupon-attempts";
    const shopIcon = "https://gw.alicdn.com/tps/TB1IrlUOXXXXXcfaXXXXXXXXXXX-178-164.png";
    const restricted = /付费|收费|购买|支付|充值|扣款|扣费|开通|开卡|续费|订阅|入会|会员|关注|粉丝|兑换|积分|授权|绑定|同意|抽奖|登录|登陆|验证|已领|已过期|已失效|已抢完|结束|去使用/;
    let timer;

    function onEntry() {
        return location.href === entry && document.visibilityState === "visible";
    }

    function visible(el) {
        if (!el || !el.getClientRects().length) return false;
        for (let node = el; node; node = node.parentElement) {
            const style = getComputedStyle(node);
            if (node.hidden || node.inert || node.getAttribute("aria-hidden") === "true" ||
                style.display === "none" || style.visibility !== "visible" || Number(style.opacity) === 0) return false;
        }
        return true;
    }

    function dateValue(stamp) {
        const [year, month, day, hour, minute] = stamp.match(/\d+/g).map(Number);
        const date = new Date(year, month - 1, day, hour, minute);
        if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day ||
            date.getHours() !== hour || date.getMinutes() !== minute) return NaN;
        return date.getTime();
    }

    function currentPeriod(text) {
        const parts = /^有效期\s+(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})\s*-\s*(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})$/.exec(text.trim());
        const now = Date.now();
        return parts && dateValue(parts[1]) <= now && now < dateValue(parts[2]);
    }

    function claimButton() {
        if (!onEntry() || [...document.querySelectorAll('dialog[open],[role="dialog"],[role="alertdialog"],[aria-modal="true"],iframe,input[type="password"],input[autocomplete="one-time-code"]')].some(visible)) return null;
        const scrollers = document.querySelectorAll('div.rax-scrollview[data-spm-protocol="i"]');
        if (!scrollers.length) return undefined;
        if (scrollers.length !== 1) return null;
        const section = scrollers[0].querySelector(":scope > div > div > div:first-child");
        if (!section || !section.querySelector('[role="button"]')) return undefined;
        if (/请.{0,4}登录|立即登录|登录领取|账号登录|短信登录|请完成验证|安全验证/.test(document.body.innerText)) return null;
        if (section.children.length !== 2 || section.closest("a[href],form") || restricted.test(section.innerText) ||
            section.querySelector('a,form,input,select,textarea,button,[aria-disabled="true"],[aria-busy="true"]')) return null;

        const [coupon, actions] = section.children;
        if (!coupon.matches("div") || !actions.matches("div") ||
            coupon.children.length !== 1 || actions.children.length !== 1) return null;
        const card = coupon.firstElementChild, button = actions.firstElementChild;
        if (!card.matches("div") || card.children.length !== 7 ||
            !button.matches('div[role="button"]') || button.children.length !== 1 ||
            section.querySelectorAll('[role="button"]').length !== 1) return null;
        // Rax serializes the active div's boolean as disabled="false".
        if ([...section.querySelectorAll("[disabled]")].some(el => el !== button ||
            el.getAttribute("disabled") !== "false")) return null;

        const [header, footer, title, time, icon, price, terms] = card.children;
        const label = button.firstElementChild;
        if (!header.matches("img") || !footer.matches("img") || !icon.matches("img") || icon.src !== shopIcon ||
            !title.matches("span") || title.childElementCount || !/^.+店铺优惠券$/.test(title.innerText.trim()) ||
            !time.matches("div") || time.children.length !== 3 ||
            !Array.from(time.children).every(el => el.matches("span") && !el.childElementCount) ||
            time.children[0].textContent.trim() || time.children[2].textContent.trim() ||
            !currentPeriod(time.children[1].innerText) || !price.matches("div") || price.children.length !== 2 ||
            !Array.from(price.children).every(el => el.matches("span") && !el.childElementCount) ||
            !/^[¥￥]$/.test(price.children[0].innerText.trim()) || !/^\d+(?:\.\d{1,2})?$/.test(price.children[1].innerText.trim()) ||
            Number(price.children[1].innerText) <= 0 || !terms.matches("span") || terms.childElementCount ||
            !/^(?:无条件使用|满\s+\d+(?:\.\d{1,2})?\s+使用)$/.test(terms.innerText.trim()) ||
            !label.matches("span") || label.childElementCount || label.innerText.trim() !== "确认领取" ||
            button.innerText.trim() !== "确认领取" || (button.hasAttribute("aria-label") && button.getAttribute("aria-label") !== "确认领取") ||
            ![title,time.children[1],...price.children,terms,button,label].every(visible)) return null;
        return button;
    }

    function hit(button) {
        const r = button.getBoundingClientRect();
        const hitElement = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return hitElement === button || hitElement === button.firstElementChild;
    }

    async function attempt(button) {
        const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(seller + "." + activity.toLowerCase()));
        const id = Array.from(new Uint8Array(hash), byte => byte.toString(16).padStart(2, "0")).join("");
        await navigator.locks.request(storageKey, () => {
            if (claimButton() !== button || !hit(button)) return;
            const day = new Date(Date.now() + 8 * 3600000).toISOString().slice(0, 10);
            const saved = JSON.parse(localStorage.getItem(storageKey) || "null");
            const ids = saved?.day === day ? saved.ids : [];
            if (!Array.isArray(ids) || ids.includes(id)) return;
            localStorage.setItem(storageKey, JSON.stringify({ day, ids: [...ids, id] }));
            button.click();
        });
    }

    function start() {
        clearTimeout(timer);
        if (!onEntry() || !navigator.locks || !window.crypto?.subtle) return;
        const until = Date.now() + 10000;
        function inspect() {
            const button = claimButton();
            if (button && hit(button)) attempt(button).catch(() => {});
            else if (button === undefined && Date.now() < until) timer = setTimeout(inspect, 300);
        }
        inspect();
    }

    window.addEventListener("hashchange", start);
    document.addEventListener("visibilitychange", start);
    window.addEventListener("pagehide", () => clearTimeout(timer));
    start();
})();
