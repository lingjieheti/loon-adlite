# YouTube 网页广告助手

在 iPhone 或 iPad 的 Safari 看 YouTube 时，这个可选脚本能收起部分列表广告，并在广告允许跳过时尝试帮你点一下按钮。

| 位置 | 实际效果 |
| --- | --- |
| 首页、搜索结果 | 隐藏能明确识别的独立广告位，旁边的普通视频仍会显示。广告素材可能已经加载。 |
| 普通视频播放页 | 在播放器进入广告状态并显示唯一、可操作的官方跳过按钮时，尝试点击一次。倒计时结束前、不可跳过的广告以及创作者录进视频的推广仍会播放。 |
| YouTube 原生 App、Shorts、第三方嵌入视频 | 此 Safari 助手未覆盖。原生 App 的片头、中插广告仍可能出现。 |

## 在 iPad 上启用

1. 在 Safari 启用 [Userscripts 扩展](https://apps.apple.com/app/id1463298887)。
2. 用 Safari [打开 YouTube 助手脚本](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)，在扩展菜单中打开 Userscripts，点安装。也可以将下载的 `youtube.user.js` 保存到已选的脚本目录，再打开一次扩展菜单。[Userscripts 安装说明](https://github.com/quoid/userscripts#ios-ipados)
3. 在 Safari 打开 [YouTube 网页](https://www.youtube.com/)，允许扩展在你使用的 YouTube 站点运行，刷新页面。播放器布局变化或要求本人点击时，仍可手动点官方跳过按钮。

助手只在 `www.youtube.com` 和 `m.youtube.com` 的顶层网页运行，无需 Loon 证书，也不读取 Cookie、保存观看记录或发送网络请求。关闭 Userscripts 中的「YouTube 网页广告助手」并刷新即可停用。

这里沿用播放器本身区分可跳过与不可跳过广告的方式。列表广告位依据公开网页组件识别，不按「广告」「赞助」等文字删除普通内容。离线测试验证的是控件识别和点击行为，实际播放取决于 YouTube 当前提供的界面。[YouTube 广告格式](https://support.google.com/youtube/answer/2467968?hl=zh-Hans) · [移动播放器样式](https://m.youtube.com/s/player/6b3d0364/mweb.css) · [EasyList 广告位记录](https://github.com/easylist/easylist/blob/25c34f4d85f863466cf6efb8232bb55a20c6c5fb/easylist/easylist_specific_hide.txt#L8865-L8884)
