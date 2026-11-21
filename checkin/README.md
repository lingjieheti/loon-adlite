# iPad 每日签到助手

在 Safari 登录自己的账号后，打开下面的专用入口，助手会检查当天状态，条件吻合时点击一次官网的签到按钮。日常逛京东或什么值得买时不会触发。可以单独使用，也可以搭配 Loon 的京东提醒。

| 服务 | 专用入口 | 会做什么 |
| --- | --- | --- |
| 京东 | [打开「我的京豆」尝试签到](https://bean.jd.com/myJingBean/list#loon-checkin) | 只处理「签到领京豆」卡片。需要同时识别今天待签、真实的签到进度和可操作按钮。京豆到账可在京东明细中核对。 |
| 什么值得买 | [打开值得买尝试签到](https://www.smzdm.com/#loon-checkin) | 登录后，在首页顶部识别「签到领奖」按钮并尝试点击。签到后可在同一处查看官网显示的连续签到天数。 |

## 第一次使用

1. 在 iPad 安装并打开 Safari 扩展 [Userscripts](https://apps.apple.com/app/id1463298887)，按应用提示设定脚本目录。在「设置 → App → Safari → 扩展」启用它。
2. 用 Safari [打开签到脚本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js)，从 Safari 的扩展菜单打开 Userscripts，选择安装。也可以把下载的 `daily.user.js` 放入已设定的脚本目录，再打开一次扩展菜单。[扩展作者的安装说明](https://github.com/quoid/userscripts#ios-ipados)
3. 在 Safari 登录想用的官网，然后从上表打开对应入口。按 Safari 提示允许扩展在该站点运行。如果登录后回到了普通首页，再点一次专用入口。保留网址末尾的 `#loon-checkin`。

## 每天怎么用

- **自动打开签到页**　在 iPad「快捷指令 → 自动化」中为一个常用的解锁时段创建「特定时间 → 每天」，选「立即运行」，用打开 URL 的操作在 Safari 打开上表中的一个完整网址。两个站点请分开时段，让每个页面都有机会在前台加载。锁屏或系统要求解锁时，等 Safari 能显示页面后再签到。[Apple 个人自动化说明](https://support.apple.com/zh-cn/guide/shortcuts/apd690170742/ios)
- **京东提醒**　需要提醒时，用 Safari [安装 Loon 京东提醒](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2Fcheckin%2FJD-reminder.lpx)。启用这个独立插件、允许 Loon 通知，Loon 运行时按设备当地时间每天 09:00 提醒一次。点通知进入京豆页。只安装提醒也可以手动签到。[提醒订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/JD-reminder.lpx)

## 签到结果与隐私

同一浏览器里，每个站点每个北京时间自然日最多自动尝试一次。网络中断后，请先看官网签到状态或奖励明细，再决定是否手动操作。首次签到缺少进度、活动换版、出现验证或要求在 App 内继续时，助手会留给本人处理。京东 App 可从「我的 → 京豆」查看明细。[京豆到账说明](https://help.jd.com/user/issue/167-4456.html) · [值得买每日签到说明](https://zhiyou.smzdm.com/user/tequan/)

这个脚本不读取 Cookie、密码、账号名或积分余额。它只在对应网站的本地存储记下最近一次尝试的日期。账号登录、验证和签到请求均由官网处理。可随时在 Userscripts 中停用脚本，在 Loon 插件列表中单独停用提醒。

京东卡片的识别依据来自京东公开发布的前端组件和一次有日期的电脑端实测。待签和已签两种状态可能使用同一张按钮图，页面加载失败时还可能显示示例进度。测试覆盖这些情况；实际账号的签到状态和奖励以官网为准。[京东网页组件配置](https://storage.360buyimg.com/assets-fe/mybean/config-js/global.js) · [京豆卡片实测记录](https://github.com/huntingrin/jd-bean-claim/blob/d07d3a40a92074f73575d4cff4de0367d01aef91/SKILL.md#每日签到)
