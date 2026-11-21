// Loon passes only the settings selected in Shopping-rewards.lpx.
const settings = typeof $argument === "object" && $argument ? $argument : {};
const guide = "https://github.com/lingjieheti/loon-adlite/blob/main/checkin/README.md";
const activities = new Map([
    ["三平台清单", [guide, "选择京东领券、淘宝红包签到或抖音商城活动。"]],
    ["京东京豆签到", ["https://bean.jd.com/myJingBean/list#loon-checkin", "打开我的京豆。已启用签到助手时会尝试签到。"]],
    ["京东领券中心", ["https://apps.apple.com/cn/app/id414245413", "轻点后在 App Store 打开京东，进入首页「领券」选券。"]],
    ["淘宝红包签到", ["https://pages-fast.m.taobao.com/wow/z/vip/hbqd5/hbqd5.0", "打开淘宝官方活动，按当天页面提示签到领红包。"]],
    ["淘宝淘金币", ["https://pages-fast.m.taobao.com/wow/z/tmtjb/town/home", "打开官方金币频道，在淘宝内签到领今日金币。"]],
    ["抖音商城领券", ["snssdk1128://mall/xtab", "轻点尝试打开抖音商城，选择当期优惠券。也可直接在抖音里点「商城」。"]],
]);

function couponEntry(raw) {
    if (typeof raw !== "string" || raw.length > 2048) return null;
    const base = "https://coupon.m.jd.com/coupons/show.action";
    const pasted = raw.trim().replace(/#loon-coupon$/, "");
    if (!pasted.startsWith(base + "?")) return null;
    const ids = new Map();
    for (const item of pasted.slice(base.length + 1).split("&")) {
        const pair = /^([A-Za-z0-9_]+)=([A-Za-z0-9._~-]+)$/.exec(item);
        if (!pair) return null;
        const [, key, value] = pair;
        if (/^(utm_[a-z0-9_]+|sceneval|scene)$/i.test(key)) continue;
        if (!["linkKey", "key", "roleId"].includes(key) || ids.has(key)) return null;
        ids.set(key, value);
    }
    const token = /^[A-Za-z0-9_-]{1,200}$/;
    let query;
    if (ids.size === 1 && ids.has("linkKey") && token.test(ids.get("linkKey"))) {
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
} else if (!entry) {
    title = "三平台清单";
    entry = activities.get(title);
}
$notification.post("每日签到领券", title, entry[1], { openUrl: entry[0] });
$done();
