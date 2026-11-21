// ==UserScript==
// @name         京东 · 领取我选的一张券
// @namespace    https://github.com/lingjieheti/loon-adlite
// @version      1.0.0
// @updateURL    https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/jd-coupon.user.js
// @description  在带专用标记的京东单券页，尝试点击一次普通优惠券的领取按钮。
// @match        https://coupon.m.jd.com/coupons/show.action*
// @run-at       document-idle
// @inject-into  content
// @noframes
// @grant        none
// ==/UserScript==

(() => {
    "use strict";

    const originAndPath = "https://coupon.m.jd.com/coupons/show.action";
    const coupon = location.search;
    if (window.self !== window.top || location.href.split("#")[0] !== originAndPath + coupon ||
        !/^\?(?:key=[A-Za-z0-9_-]{1,200}&roleId=[0-9]{1,20}|linkKey=[A-Za-z0-9_-]{1,200})$/.test(coupon)) return;

    const entry = originAndPath + coupon + "#loon-coupon";
    const storageKey = "loon-adlite:jd:coupon-attempts";
    const restricted = /付费|收费|有价券|购券|付[款钱]|支付|购买|充值|扣款|扣费|开通|开卡|续费|订阅|入会|会员|PLUS|关注|粉丝|膨胀|兑换|京豆|积分|抽奖|白条|绑定|授权|预约|去使用|立即使用|已领取|已领完|已过期|活动已结束|登录|验证|打开.{0,4}App|前往.{0,4}App/i;
    let timer;

    function onEntry() {
        return location.href === entry && document.visibilityState === "visible";
    }

    function only(parent, selector) {
        const found = parent.querySelectorAll(selector);
        return found.length === 1 ? found[0] : null;
    }

    function visible(element) {
        if (!element || !element.getClientRects().length) return false;
        for (let node = element; node; node = node.parentElement) {
            const style = getComputedStyle(node);
            if (node.hidden || node.inert || node.getAttribute("aria-hidden") === "true" ||
                style.display === "none" || style.visibility !== "visible" || Number(style.opacity) === 0) return false;
        }
        return true;
    }

    // undefined means the official card has not rendered yet. A recognized refusal ends this attempt.
    function claimButton() {
        if (!onEntry() || [...document.querySelectorAll('dialog[open],[role="dialog"],[role="alertdialog"],[aria-modal="true"],.mod_alert_v2,.mod_alert')].some(visible)) return null;
        const wrapper = only(document, "#root .wx_wrap");
        if (!wrapper) return undefined;
        const card = only(wrapper, ":scope > .mjd-coupon > .coupon-box");
        const actions = only(wrapper, ":scope > .coupon-btns");
        if (!card || !actions) return undefined;
        if (!visible(card) || !visible(actions) || actions.children.length !== 1 ||
            card.querySelector(".fans,.mark-vip,.mark-jt,.revevied") || restricted.test(card.innerText + " " + actions.innerText)) return null;

        const value = only(card, ":scope > .coupon-value > .coupon-content");
        const scope = only(card, ":scope > .coupon-info > .info-content > p.use-rule");
        if (!visible(value) || !visible(scope) || !scope.innerText.trim()) return null;
        const price = only(value, ":scope > p.money, :scope > p.discount-money");
        const rule = only(value, ":scope > p.rule");
        if (!price || !rule) return null;
        const amount = only(price, ":scope > strong");
        const discount = price.matches(".discount-money");
        const unit = only(price, discount ? ":scope > span" : ":scope > em");
        if (!visible(amount) || !visible(unit) || !/^\d+(?:\.\d+)?$/.test(amount.innerText.trim()) ||
            Number(amount.innerText) <= 0 || (discount && Number(amount.innerText) >= 10) ||
            !(discount ? /^折$/ : /^[¥￥]$/).test(unit.innerText.trim())) return null;
        // JD can leave the rule empty for a coupon without a minimum spend.
        const terms = rule.textContent.trim();
        if (terms && (!visible(rule) || !/^(?:无门槛|(?:每)?满\s*\d+(?:\.\d+)?\s*元可用)$/.test(terms))) return null;

        const button = actions.firstElementChild;
        const label = button.getAttribute("aria-label");
        if (!button.matches("div.btn") || button.children.length || !visible(button) || button.innerText.trim() !== "立即领取" ||
            button.matches(".grey,.disabled,[disabled],[aria-disabled=true],[aria-busy=true],[formaction]") ||
            button.closest("a[href],form,[inert]") || (label && label !== "立即领取")) return null;
        return button;
    }

    function hit(button) {
        const rect = button.getBoundingClientRect();
        return document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2) === button;
    }

    async function attempt(button) {
        const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(coupon));
        const id = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
        await navigator.locks.request(storageKey, () => {
            if (claimButton() !== button || !hit(button)) return;
            const today = new Date(Date.now() + 8 * 3600000).toISOString().slice(0, 10);
            const saved = JSON.parse(localStorage.getItem(storageKey) || "null");
            const ids = saved?.day === today ? saved.ids : [];
            if (!Array.isArray(ids) || ids.includes(id)) return;
            localStorage.setItem(storageKey, JSON.stringify({ day: today, ids: [...ids, id] }));
            button.click();
        });
    }

    function start() {
        clearTimeout(timer);
        if (!onEntry() || !navigator.locks || !window.crypto?.subtle) return;
        const until = Date.now() + 10000;
        let scrolled = false;
        function inspect() {
            const button = claimButton();
            if (button && hit(button)) {
                // Storage may be unavailable. In that case the official control remains usable.
                attempt(button).catch(() => {});
            } else if (button && !scrolled) {
                const r = button.getBoundingClientRect();
                if (r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth) return;
                scrolled = true;
                button.scrollIntoView({ block: "center", inline: "nearest", behavior: "instant" });
                timer = setTimeout(inspect, 0);
            } else if (button === undefined && Date.now() < until) {
                timer = setTimeout(inspect, 300);
            }
        }
        inspect();
    }

    window.addEventListener("hashchange", start);
    document.addEventListener("visibilitychange", start);
    window.addEventListener("pagehide", () => clearTimeout(timer));
    start();
})();
