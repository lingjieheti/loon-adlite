$notification.post(
  "京东签到提醒",
  "",
  "轻点打开「我的京豆」。已安装网页助手可尝试自动签到，也可手动签到。结果以京东页面为准。",
  { openUrl: "https://bean.jd.com/myJingBean/list#loon-checkin" }
);
$done();
