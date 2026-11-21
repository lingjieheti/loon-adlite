"""Exercise the optional JD reminder without Loon, a network, or an account."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


CHECKIN = Path(__file__).resolve().parents[1] / "checkin"
ENTRY_URL = "https://bean.jd.com/myJingBean/list#loon-checkin"
RAW_REPO = "https://raw.githubusercontent.com/lingjieheti/loon-adlite"


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
        harness = """
            const fs = require("node:fs");
            const vm = require("node:vm");
            const events = [];
            const api = {
                $notification: {post: (...args) => events.push(["notify", ...args])},
                $done: (...args) => events.push(["done", ...args])
            };
            for (const key of ["$httpClient", "$persistentStore", "$request", "$response", "$dns", "fetch"]) {
                Object.defineProperty(api, key, {get() {
                    events.push(["unexpected access", key]);
                    throw new Error(key);
                }});
            }
            vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), api, {timeout: 1000});
            process.stdout.write(JSON.stringify(events));
        """
        result = subprocess.run(
            ["node", "-e", harness, str(CHECKIN / "jd-reminder.js")],
            capture_output=True, check=True, encoding="utf-8", timeout=10,
        )
        notification, done = json.loads(result.stdout)
        self.assertEqual(done, ["done"])
        event, title, subtitle, content, attachment = notification
        self.assertEqual(event, "notify")
        self.assertIn("提醒", title)
        self.assertIn("手动签到", content)
        self.assertNotIn("签到成功", title + subtitle + content)
        self.assertEqual(attachment, {"openUrl": ENTRY_URL})
