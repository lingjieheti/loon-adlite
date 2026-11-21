// Loon passes only the settings selected in Shopping-rewards.lpx.
const settings = typeof $argument === "object" && $argument ? $argument : {};
const guide = "https://github.com/lingjieheti/loon-adlite/blob/main/checkin/README.md";
const activities = new Map([
    ["三平台清单", [guide, "选择京东领券、淘宝红包签到、淘宝店铺券或抖音商城活动。"]],
    ["京东京豆签到", ["https://bean.jd.com/myJingBean/list#loon-checkin", "打开我的京豆。已启用签到助手时会尝试签到。"]],
    ["京东领券中心", ["https://apps.apple.com/cn/app/id414245413", "轻点后在 App Store 打开京东，进入首页「领券」选券。"]],
    ["淘宝红包签到", [openTaobao("https://pages-fast.m.taobao.com/wow/z/vip/hbqd5/hbqd5.0"), "打开淘宝红包签到页，按当天页面提示领红包。"]],
    ["淘宝淘金币", [openTaobao("https://pages-fast.m.taobao.com/wow/z/tmtjb/town/home"), "打开淘宝金币频道，在活动页签到领今日金币。"]],
    ["抖音商城领券", ["snssdk1128://mall/xtab", "轻点尝试打开抖音商城，选择当期优惠券。也可直接在抖音里点「商城」。"]],
]);

function openTaobao(officialUrl) {
    if (settings.taobaoOpen === "网页") return officialUrl;
    return "taobao://m.taobao.com/tbopen/index.html?h5Url=" + encodeURIComponent(officialUrl);
}

function taobaoCouponEntry(raw) {
    const base = "https://taoquan.taobao.com/coupon/unify_apply.htm";
    if (typeof raw !== "string" || raw.length > 2048) return null;
    const pasted = raw.trim();
    if (!pasted.startsWith(base + "?") || /[\s#\\]/.test(pasted)) return null;
    let sellerId, activityId;
    for (const item of pasted.slice(base.length + 1).split("&")) {
        const pair = /^([A-Za-z0-9_]+)=([^&]*)$/.exec(item);
        if (!pair) return null;
        const [, key, value] = pair;
        if (key === "sellerId" && sellerId === undefined && /^[1-9][0-9]{0,19}$/.test(value)) {
            sellerId = value;
        } else if (key === "activityId" && activityId === undefined && /^[A-Fa-f0-9]{32}$/.test(value)) {
            activityId = value;
        } else if (!/^(?:spm|scm|acm|utm_[a-z0-9_]+)$/i.test(key)) {
            return null;
        }
    }
    if (!sellerId || !activityId) return null;
    const officialUrl = base + "?sellerId=" + sellerId + "&activityId=" + activityId;
    if (settings.taobaoOpen === "网页") {
        // The official page parses the whole URL. Keep our fragment out of the last activity ID.
        return officialUrl + "&#loon-coupon=" + sellerId + "." + activityId;
    }
    return openTaobao(officialUrl);
}

function couponEntry(raw) {
    if (typeof raw !== "string" || raw.length > 2048) return null;
    const base = "https://coupon.m.jd.com/coupons/show.action";
    const pasted = raw.trim();
    const desktop = /^https?:\/\/coupon\.jd\.com\/ilink\/couponSendFront\/send_index\.action\?/.exec(pasted);
    if (!desktop && !pasted.startsWith(base + "?")) return null;
    const inputQuery = desktop ? pasted.slice(desktop[0].length)
        : pasted.slice(base.length + 1).replace(/#loon-coupon$/, "");
    const ids = new Map();
    let hasStore = false;
    for (const item of inputQuery.split("&")) {
        // Desktop shop links can include a post-claim destination. Discard it locally.
        if (desktop && item.startsWith("to=")) {
            const store = /^to=(?:[a-z0-9-]+\.)+jd\.com(?:\/[a-z0-9_-][a-z0-9._~-]*)*\/?$/i;
            if (hasStore || !store.test(item)) return null;
            hasStore = true;
            continue;
        }
        const pair = /^([A-Za-z0-9_]+)=([A-Za-z0-9._~-]+)$/.exec(item);
        if (!pair) return null;
        const [, key, value] = pair;
        if (/^(utm_[a-z0-9_]+|sceneval|scene)$/i.test(key)) continue;
        if (!["linkKey", "key", "roleId"].includes(key) || ids.has(key)) return null;
        ids.set(key, value);
    }
    const token = /^[A-Za-z0-9_-]{1,200}$/;
    let query;
    if (!desktop && ids.size === 1 && ids.has("linkKey") && token.test(ids.get("linkKey"))) {
        query = "linkKey=" + ids.get("linkKey");
    } else if (ids.size === 2 && ids.has("key") && ids.has("roleId") &&
               token.test(ids.get("key")) && /^[0-9]{1,20}$/.test(ids.get("roleId"))) {
        query = "key=" + ids.get("key") + "&roleId=" + ids.get("roleId");
    } else {
        return null;
    }
    return base + "?" + query + "#loon-coupon";
}

let title = settings.destination;
let entry = activities.get(title);
if (title === "京东指定优惠券") {
    const url = couponEntry(settings.coupon);
    entry = url
        ? [url, "轻点打开你选定的单券。Safari 领券助手只尝试普通领取，到账请查京东券包。"]
        : [guide, "请在插件设置粘贴京东官方单券链接。轻点查看支持的链接格式。"];
} else if (title === "淘宝店铺券") {
    const url = taobaoCouponEntry(settings.taobaoCoupon);
    entry = url
        ? [url, settings.taobaoOpen === "网页"
            ? "打开你选定的店铺券。若已启用 Safari 淘宝单券助手，会尝试领取普通店铺券。"
            : "打开你选定的淘宝店铺券，核对门槛和有效期后在淘宝内领取。"]
        : [guide, "请在插件设置粘贴淘宝官方店铺券链接。轻点查看支持的链接格式。"];
} else if (!entry) {
    title = "三平台清单";
    entry = activities.get(title);
}
$notification.post("每日签到领券", title, entry[1], { openUrl: entry[0] });
$done();
