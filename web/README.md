# iPhone 和 iPad 网页广告过滤

**已安装 Loon 轻量版或合并版**，刷新现有订阅即可获得网页域名规则。Loon 会拦截发往已知广告主机的请求，包括部分常见网页广告竞价及 Pornhub 上使用的第三方广告服务。新增规则只按完整主机名匹配，无需为这些网站安装证书或开启 HTTPS 解密。[版本与订阅](../README.md#安装) · [主机清单与来源](../COVERAGE.md)

## 在 Safari 隐藏 Pornhub 网页广告位

1. 在 iPad 或 iPhone 上启用 Safari 的 Userscripts 扩展。如果已经使用本项目的 YouTube 或签到助手，沿用原来的脚本目录即可。[Userscripts](https://apps.apple.com/app/id1463298887)
2. 用 Safari 打开脚本，在扩展菜单内选择 Userscripts 并安装。如果 `pornhub.user.js` 已在选定的脚本目录，直接打开扩展菜单确认它已启用即可。[打开脚本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js) · [扩展安装说明](https://github.com/quoid/userscripts#ios-ipados)
3. 允许扩展在你使用的目标站点运行，然后刷新页面。以后可在 Userscripts 中检查脚本更新；停用后刷新页面即可恢复原布局。

脚本在 `pornhub.com` 及其子域的 HTTPS 顶层页面上添加一张样式表，可隐藏侧栏横幅、移动播放页的指定广告位、带有 TrafficJunky 标记的广告元素及直接指向广告服务器的链接。后来插入的匹配元素也会被隐藏。脚本不扫描页面文字、不读取 Cookie，也不发送浏览数据。[EasyList 侧栏规则](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L883) · [EasyList 投放链接规则](https://github.com/easylist/easylist/blob/f02e1e02a696e62ba2fadefb9fa9df0ad3f80cf0/easylist_adult/adult_specific_hide.txt#L1265) · [AdGuard 移动页面规则](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/MobileFilter/sections/specific_web.txt#L6194-L6200) · [AdGuard 广告元素规则](https://github.com/AdguardTeam/AdguardFilters/blob/3e12a9344bec9b7591af533217e7a15cf9ade5b3/BaseFilter/sections/specific.txt#L5549)

**弹出式广告**可在「设置 → App → Safari 浏览器」打开「阻止弹出式窗口」。域名拦截可以阻止匹配的广告地址加载，站点仍可能打开空白标签页。[Apple 设置说明](https://support.apple.com/zh-cn/102524)

**视频片头和中插**如果与正片合为同一条媒体流，仍会播放。离线测试检查广告位的可见性、正常视频和确认按钮等控件，以及在其他域名和子框架中的行为。真实站点的投放、地区和页面布局会变化。[网页回归用例](../tests/web_ads_browser.py)
