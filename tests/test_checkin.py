"""Exercise the optional reminders without Loon, a network, or an account."""

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


CHECKIN = Path(__file__).resolve().parents[1] / "checkin"
ENTRY_URL = "https://bean.jd.com/myJingBean/list#loon-checkin"
RAW_REPO = "https://raw.githubusercontent.com/lingjieheti/loon-adlite"
GUIDE = "https://github.com/lingjieheti/loon-adlite/blob/main/checkin/README.md"
COUPON = "https://coupon.m.jd.com/coupons/show.action"
SINGLE_COUPON = "京东指定优惠券"
DESTINATIONS = {
    "三平台清单": GUIDE,
    "京东领券中心": "https://apps.apple.com/cn/app/id414245413",
    SINGLE_COUPON: GUIDE,  # A missing coupon link opens the configuration guide.
    "京东京豆签到": ENTRY_URL,
    "淘宝红包签到": "https://pages-fast.m.taobao.com/wow/z/vip/hbqd5/hbqd5.0",
    "淘宝淘金币": "https://pages-fast.m.taobao.com/wow/z/tmtjb/town/home",
    "抖音商城领券": "snssdk1128://mall/xtab",
}


def run_reminder(script, settings):
    harness = """
        const fs = require("node:fs"), vm = require("node:vm");
        const source = fs.readFileSync(process.argv[1], "utf8");
        const runs = JSON.parse(fs.readFileSync(0, "utf8")).map(argument => {
            const events = [];
            const api = {
                $notification: {post: (...args) => events.push(["notify", ...args])},
                $done: (...args) => events.push(["done", ...args]),
            };
            if (argument !== null) api.$argument = argument;
            for (const key of ["$httpClient", "$persistentStore", "$request", "$response", "$dns",
                               "$httpAPI", "fetch", "XMLHttpRequest", "localStorage"]) {
                Object.defineProperty(api, key, {get() {
                    events.push(["unexpected access", key]);
                    throw new Error(key);
                }});
            }
            vm.runInNewContext(source, api, {timeout: 1000});
            return events;
        });
        process.stdout.write(JSON.stringify(runs));
    """
    result = subprocess.run(["node", "-e", harness, str(CHECKIN / script)], input=json.dumps(settings),
                            capture_output=True, check=True, encoding="utf-8", timeout=10)
    return json.loads(result.stdout)


class CheckinTests(unittest.TestCase):
    def test_plugin_schedules_only_the_pinned_reminder(self):
        plugin = (CHECKIN / "JD-reminder.lpx").read_text(encoding="utf-8")
        directives = [line.strip() for line in plugin.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        self.assertEqual(len(directives), 2)
        self.assertEqual(directives[0], "[Script]")
        rule = re.fullmatch(
            rf'cron "0 9 \* \* \*" script-path={re.escape(RAW_REPO)}/([0-9a-f]{{40}})/checkin/jd-reminder\.js'
            r'(?:,(?:tag=[^,]+|timeout=\d+))*',
            directives[1],
        )
        self.assertIsNotNone(rule, directives[1])
        # A full local checkout can verify the resolved revision without a network call.
        # Release validation checks the raw URL separately for shallow CI checkouts.
        if (CHECKIN.parent / ".git").exists() and shutil.which("git"):
            git = ["git", "-C", str(CHECKIN.parent)]
            shallow = subprocess.check_output([*git, "rev-parse", "--is-shallow-repository"], text=True)
            if shallow.strip() == "false":
                pinned = subprocess.check_output([*git, "show", f"{rule[1]}:checkin/jd-reminder.js"])
                local = (CHECKIN / "jd-reminder.js").read_text(encoding="utf-8")
                self.assertEqual(pinned.decode("utf-8").replace("\r\n", "\n"), local)

    def test_reminder_posts_one_notification_then_finishes(self):
        (notification, done), = run_reminder("jd-reminder.js", [None])
        self.assertEqual(done, ["done"])
        event, title, subtitle, content, attachment = notification
        self.assertEqual(event, "notify")
        self.assertIn("提醒", title)
        self.assertIn("手动签到", content)
        self.assertNotIn("签到成功", title + subtitle + content)
        self.assertEqual(attachment, {"openUrl": ENTRY_URL})

    def test_shopping_plugin_choices_and_pinned_script(self):
        source = (CHECKIN / "Shopping-rewards.lpx").read_text(encoding="utf-8")
        lines = [line.strip() for line in source.splitlines() if line.strip() and not line.startswith("#")]
        section, destinations, coupon, hours, script_section, script = lines
        self.assertEqual((section, script_section), ("[Argument]", "[Script]"))
        self.assertEqual(destinations.partition(",tag=")[0],
                         "destination = select," + ",".join(f'"{key}"' for key in DESTINATIONS))
        self.assertTrue(coupon.startswith("coupon = input,tag="))
        self.assertEqual(hours.partition(",tag=")[0], 'hour = select,"0 9 * * *","0 12 * * *","0 20 * * *"')
        revision = "6c18f0edb49c6c7dc3968e2f97f8ed79fabf03e6"
        self.assertEqual(script, 'cron ${hour} then script("' + RAW_REPO + "/" + revision
                         + '/checkin/shopping-reminder.js", {${destination}, ${coupon}}) with tag="签到领券", timeout=5')
        # Digest of the pinned file, also verifiable in a shallow checkout.
        local = (CHECKIN / "shopping-reminder.js").read_text(encoding="utf-8").encode()
        self.assertEqual(hashlib.sha256(local).hexdigest(), "9af864550d08f4de28e3ad0609f5814f4807665804acaa251bfe6489d0a0206b")

    def test_shopping_notifications_and_selected_coupon(self):
        cases = [({"destination": key}, key, url) for key, url in DESTINATIONS.items()]
        cases += [(arg, "三平台清单", GUIDE) for arg in (None, {"destination": "unknown"}, "invalid")]
        for query, canonical in (
            ("?linkKey=A_1-2&utm_source=test", "?linkKey=A_1-2"),
            ("?roleId=12&sceneval=2&key=Ab#loon-coupon", "?key=Ab&roleId=12"),
        ):
            cases.append(({"destination": SINGLE_COUPON, "coupon": COUPON + query}, SINGLE_COUPON,
                          COUPON + canonical + "#loon-coupon"))
        for bad in (COUPON.replace("jd.com", "jd.com.example.org") + "?linkKey=A",
                    COUPON.replace("https:", "http:") + "?linkKey=A",
                    COUPON + "?key=abc", COUPON + "?linkKey=A&linkKey=B", COUPON + "?roleId=x&key=A",
                    COUPON + "?linkKey=A&redirect=foreign", COUPON + "?linkKey=A#foreign"):
            cases.append(({"destination": SINGLE_COUPON, "coupon": bad}, SINGLE_COUPON, GUIDE))
        results = run_reminder("shopping-reminder.js", [arg for arg, _, _ in cases])
        self.assertEqual(len(results), len(cases))
        for (arg, label, url), (notification, done) in zip(cases, results):
            with self.subTest(settings=arg):
                event, title, subtitle, content, attachment = notification
                self.assertEqual((event, title, subtitle, attachment, done),
                                 ("notify", "每日签到领券", label, {"openUrl": url}, ["done"]))
                self.assertNotRegex(content, r"已签到|签到成功|已领取|领取成功|已到账")
                if label == SINGLE_COUPON:
                    self.assertIn("设置" if url == GUIDE else "尝试", content)
