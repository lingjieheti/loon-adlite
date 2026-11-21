# 京东、淘宝、抖音每日签到领券

把这页加入 Safari 书签，就能在 iPhone 或 iPad 上找到三个平台的日常优惠。也可以安装一个独立的 Loon 提醒，每天从通知打开你最常用的入口。[安装签到领券提醒](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2Fcheckin%2FShopping-rewards.lpx) · [订阅地址](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/Shopping-rewards.lpx)

| 平台 | 签到 | 领券与查券 |
| --- | --- | --- |
| 京东 | [我的京豆](https://bean.jd.com/myJingBean/list#loon-checkin)可搭配下方签到脚本。 | 打开京东 App 首页的「领券」挑券。有官方单券链接时，可用下方助手尝试领取；到账后查看[我的优惠券](https://my.m.jd.com/coupon/index.html?sceneval=2)。[京东领券说明](https://help.jd.com/user/issue/169-335.html) |
| 淘宝 | [红包签到](https://pages-fast.m.taobao.com/wow/z/vip/hbqd5/hbqd5.0)或[领淘金币](https://pages-fast.m.taobao.com/wow/z/tmtjb/town/home)。如提示「前往手淘 App」，在淘宝完成当天活动。淘金币是可按规则抵扣的积分。 | 在商品或店铺活动页查看券面、门槛和有效期，选择要领的券。[我的权益 → 券](https://pages-fast.m.taobao.com/wow/bz/jingmi/1592?tabType=coupon)可查已领的券。[淘金币玩法](https://pages.tmall.com/wow/z/tmtjb/tjbTube/nchn73f3hfmnsmr8474r) |
| 抖音主 App | 「我 → ≡ → 我的钱包 → 积分」可按页面提示签到领支付积分。所引活动规则适用至 2026 年 12 月 31 日，资格和后续活动以钱包页面为准。[支付积分规则](https://lf26-cdn-tos.draftstatic.com/obj/ies-hotsoon-draft/financePayment/61d48a0f-5550-47f3-bdb5-7c8e7e28a4c9.html) | 打开「抖音 → 商城」，选择当天展示的优惠券。提醒可尝试直接打开商城；若未跳转，手动打开抖音并点「商城」。[打开抖音的 App Store 页面](https://apps.apple.com/cn/app/id1142110895) · [商城领券指南](https://apps.apple.com/cn/story/id1759101041) |

## 用 Loon 提醒打开活动

在 Loon 插件设置中选「轻点通知打开」和每日提醒时间。默认 09:00 打开三平台清单，也可选 12:00 或 20:00，均为设备当地时间。启用插件、允许 Loon 通知后，轻点当天的提醒即可。淘宝活动和抖音商城由本人在官方页面确认；京东领券中心选项通过 App Store 打开京东，再从首页点「领券」。如已有旧的「京东签到提醒」，保留一个提醒即可。新版提醒需要 Loon 3.5.1（983）或更新版本。

## 自动尝试领取自己选定的京东券

1. 在 Safari 启用 Userscripts，打开脚本并在扩展菜单中安装，允许它在 `coupon.m.jd.com` 运行。[京东单券助手](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/jd-coupon.user.js) · [Userscripts](https://apps.apple.com/app/id1463298887)
2. 在 Loon 的签到领券提醒里选「京东指定优惠券」，把自己选好的京东官方单券网址粘到「京东官方单券链接」。支持 `https://coupon.m.jd.com/coupons/show.action` 下带 `key` 和 `roleId`，或仅带 `linkKey` 的链接。也可以在不使用提醒时，给符合该格式的网址末尾加上 `#loon-coupon`，自行用 Safari 打开。
3. 轻点提醒会在前台打开这张券。助手只在能辨认出券面、使用条件及唯一「立即领取」按钮时尝试一次。登录提示、活动结束、关注店铺、付费、会员或积分兑换等情况由你在京东页面处理。领取结果以京东提示及券包为准。[京东单券页公开组件](https://storage.360buyimg.com/miniprogram-platform/m-add-sns/receive-coupon-m/main.a04e4b02.js)

提醒只在本机创建通知，无需 HTTPS 解密或提供账号 Cookie。单券地址保存在插件设置里；轻点有效的单券通知后才会打开对应的京东页面。Safari 助手按北京时间记录当天尝试过的券链接摘要，重复打开或同时打开两个标签页时，同一链接当天最多尝试一次。若第一次遇到登录提示，登录后可在官网手动领取。

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
