# 京东、淘宝、抖音每日签到领券

把这页加入 Safari 书签，就能在 iPhone 或 iPad 上找到三个平台的日常优惠。也可以安装一个独立的 Loon 提醒，每天从通知打开你最常用的入口。[安装签到领券提醒](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2Fcheckin%2FShopping-rewards.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/Shopping-rewards.lpx)

| 平台 | 签到 | 领券与查券 |
| --- | --- | --- |
| 京东 | [我的京豆](https://bean.jd.com/myJingBean/list#loon-checkin)可搭配下方签到脚本。 | 打开京东 App 首页的「领券」挑券。有官方单券链接时，可用下方助手尝试领取；到账后查看[我的优惠券](https://my.m.jd.com/coupon/index.html?sceneval=2)。[京东领券说明](https://help.jd.com/user/issue/169-335.html) |
| 淘宝 | 提醒可直达「红包签到」或「淘金币」。也可从 Safari 打开[红包签到](https://pages-fast.m.taobao.com/wow/z/vip/hbqd5/hbqd5.0)或[淘金币首页](https://pages-fast.m.taobao.com/wow/z/tmtjb/town/home)。金币抵扣条件以活动页为准。 | 提醒可以打开自己选的店铺券，核对门槛、有效期后领取。去[我的权益 → 券](https://pages-fast.m.taobao.com/wow/bz/jingmi/1592?tabType=coupon)查到账记录。 |
| 抖音主 App | 「我 → ≡ → 我的钱包 → 积分」可按页面提示签到领支付积分。所引活动规则适用至 2026 年 12 月 31 日，资格和后续活动以钱包页面为准。[支付积分规则](https://lf26-cdn-tos.draftstatic.com/obj/ies-hotsoon-draft/financePayment/61d48a0f-5550-47f3-bdb5-7c8e7e28a4c9.html) | 打开「抖音 → 商城」，选择当天展示的优惠券。提醒可尝试直接打开商城；若未跳转，手动打开抖音并点「商城」。[打开抖音的 App Store 页面](https://apps.apple.com/cn/app/id1142110895) · [商城领券指南](https://apps.apple.com/cn/story/id1759101041) |

## 用 Loon 提醒打开活动

在 Loon 3.5.1（983）或更新版本中启用插件，允许通知。在「轻点通知打开」选一个入口。默认按设备当地时间 09:00 提醒，也可改为 12:00 或 20:00。默认入口是三平台清单。若同时订阅了旧的「京东签到提醒」，启用其中一个即可。

### 淘宝红包、淘金币和店铺券

- **红包与金币**　在「轻点通知打开」选「淘宝红包签到」或「淘宝淘金币」。「淘宝打开方式」默认选「淘宝 App」，点通知会尝试直接进入对应活动。未安装淘宝或希望用 Safari 时，改选「网页」。若网页提示「前往手淘 App」，请在淘宝内继续。
- **店铺单券**　选择「淘宝店铺券」，将自己选好的店铺券领取网址粘贴到「淘宝官方店铺券链接」。支持 `https://taoquan.taobao.com/coupon/unify_apply.htm` 下同时带 `sellerId`（数字商家 ID）和 `activityId`（32 位十六进制活动 ID）的链接。默认在淘宝 App 打开这张券，由你核对门槛、有效期后领取。[淘宝官方店铺券格式](https://developer.alibaba.com/docs/doc.htm?articleId=109022&docType=1&treeId=796) · [OpenFlutter 的店铺单券直达示例（Apache-2.0）](https://github.com/OpenFlutter/nautilus/blob/787250c0f02002697b6da058a8477159a607ae0f/README.md#L46-L48)
- **用 Safari 尝试领这张券**　将「淘宝打开方式」改成「网页」，在 Safari 的 Userscripts 中单独安装[淘宝单券助手](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/taobao-coupon.user.js)，允许它在 `market.m.taobao.com` 运行。轻点提醒后，助手核对网址标记 `#loon-coupon=<sellerId>.<activityId>` 与跳转后店铺、活动两个 ID 都相符，并在官方券页识别出普通领取按钮时，才会自动尝试一次。未登录会进入淘宝登录页。红包签到和淘金币继续在活动页手动完成，实际领到的优惠券以券包为准。[淘宝公开券页组件](https://g.alicdn.com/cm/m-rx-coupon/0.1.2/pages/detail/index.web.js)

Android 开源项目分别实现了淘宝的「签到领金币」和「红包签到」。这里沿用这两个活动入口，改为从 iPhone 或 iPad 的通知直接进入。无登录测试已核实单券跳转和登录页，真实账号领券到账仍待验证。[JavisPeng 的淘金币实现（GPL-3.0）](https://github.com/JavisPeng/taojinbi/blob/e0e9638f48f863c0ddf250ce0ea30df432288dd0/taojinbi.js#L478-L488) · [TonyJiangWJ 的红包签到实现（GPL-2.0）](https://github.com/TonyJiangWJ/Unify-Sign/blob/821962e037ae0578f66acff4fc26d37dedac482f/core/Taobao-Sign.js#L53-L69) · [iOS 淘宝活动直达示例](https://gist.github.com/JamesHopbourn/046bc341e7debfd0c86e3b388d983c53/3809a04465599866323dcc8685d64bfa5332e543)

## 自动尝试领取自己选定的京东券

1. 在 Safari 启用 Userscripts，打开脚本并在扩展菜单中安装，允许它在 `coupon.m.jd.com` 运行。[京东单券助手](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/jd-coupon.user.js) · [Userscripts](https://apps.apple.com/app/id1463298887)
2. 在提醒的「轻点通知打开」选「京东指定优惠券」，把券链接粘到「京东官方单券链接」。支持手机版 `https://coupon.m.jd.com/coupons/show.action` 的 `key` ＋ `roleId` 或 `linkKey` 格式，也支持电脑版 `https://coupon.jd.com/ilink/couponSendFront/send_index.action` 的 `key` ＋ `roleId` 格式。提醒会打开对应的手机单券页。若直接用 Safari，请在该手机链接末尾加上 `#loon-coupon`。[京东桌面店铺券的公开链接样例](https://github.com/irebit/jingdong_union_go/blob/deb4c5eaa5c63a08a423ae5d3f24eec432efc30f/jd.union_test.go#L84)
3. 轻点提醒会在前台打开这张券。助手只在能辨认出券面、使用条件及唯一「立即领取」按钮时尝试一次。登录提示、活动结束、关注店铺、付费、会员或积分兑换等情况由你在京东页面处理。领取结果以京东提示及券包为准。[京东单券页公开组件](https://storage.360buyimg.com/miniprogram-platform/m-add-sns/receive-coupon-m/main.a04e4b02.js)

提醒只在本机创建通知，无需 HTTPS 解密或提供账号 Cookie。京东和淘宝的单券地址保存在 Loon 插件设置里，轻点通知后才打开对应页面。两个 Safari 单券助手分别在官网的浏览器本地存储中记录券标识的摘要，按北京时间去重。同一张淘宝券或同一条京东券链接当天最多尝试一次，同时打开两个标签页也一样。若遇到登录提示，可以在官网登录后再打开提醒，或手动领取。

## 京豆和什么值得买签到

在 Safari 登录后打开下表的专用入口，已有的签到助手会检查当天状态，条件吻合时点击一次官网的签到按钮。

| 服务 | 专用入口 | 会做什么 |
| --- | --- | --- |
| 京东 | [打开「我的京豆」尝试签到](https://bean.jd.com/myJingBean/list#loon-checkin) | 只处理「签到领京豆」卡片。需要同时识别今天待签、真实的签到进度和可操作按钮。京豆到账可在京东明细中核对。 |
| 什么值得买 | [打开值得买尝试签到](https://www.smzdm.com/#loon-checkin) | 登录后，在首页顶部识别「签到领奖」按钮并尝试点击。签到后可在同一处查看官网显示的连续签到天数。 |

### 安装签到脚本

1. 在 iPad 安装并打开 Safari 扩展 [Userscripts](https://apps.apple.com/app/id1463298887)，按应用提示设定脚本目录。在「设置 → App → Safari → 扩展」启用它。
2. 用 Safari [打开签到脚本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js)，从 Safari 的扩展菜单打开 Userscripts，选择安装。也可以把下载的 `daily.user.js` 放入已设定的脚本目录，再打开一次扩展菜单。[扩展作者的安装说明](https://github.com/quoid/userscripts#ios-ipados)
3. 在 Safari 登录想用的官网，然后从上表打开对应入口。按 Safari 提示允许扩展在该站点运行。如果登录后回到了普通首页，再点一次专用入口。保留网址末尾的 `#loon-checkin`。

### 每天怎么用

- **自动打开签到页**　在 iPad「快捷指令 → 自动化」中为一个常用的解锁时段创建「特定时间 → 每天」，选「立即运行」，用打开 URL 的操作在 Safari 打开上表中的一个完整网址。两个站点请分开时段，让每个页面都有机会在前台加载。锁屏或系统要求解锁时，等 Safari 能显示页面后再签到。[Apple 个人自动化说明](https://support.apple.com/zh-cn/guide/shortcuts/apd690170742/ios)
- **京东提醒**　需要提醒时，用 Safari [安装 Loon 京东提醒](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2Fcheckin%2FJD-reminder.lpx)。启用这个独立插件、允许 Loon 通知，Loon 运行时按设备当地时间每天 09:00 提醒一次。点通知进入京豆页。只安装提醒也可以手动签到。[提醒订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/JD-reminder.lpx)

### 签到结果与隐私

同一浏览器里，每个站点每个北京时间自然日最多自动尝试一次。网络中断后，请先看官网签到状态或奖励明细，再决定是否手动操作。首次签到缺少进度、活动换版、出现验证或要求在 App 内继续时，助手会留给本人处理。京东 App 可从「我的 → 京豆」查看明细。[京豆到账说明](https://help.jd.com/user/issue/167-4456.html) · [值得买每日签到说明](https://zhiyou.smzdm.com/user/tequan/)

这个脚本不读取 Cookie、密码、账号名或积分余额。它只在对应网站的本地存储记下最近一次尝试的日期。账号登录、验证和签到请求均由官网处理。可随时在 Userscripts 中停用脚本，在 Loon 插件列表中单独停用提醒。

京东卡片的识别依据来自京东公开发布的前端组件和一次有日期的电脑端实测。待签和已签两种状态可能使用同一张按钮图，页面加载失败时还可能显示示例进度。测试覆盖这些情况；实际账号的签到状态和奖励以官网为准。[京东网页组件配置](https://storage.360buyimg.com/assets-fe/mybean/config-js/global.js) · [京豆卡片实测记录](https://github.com/huntingrin/jd-bean-claim/blob/d07d3a40a92074f73575d4cff4de0367d01aef91/SKILL.md#每日签到)
