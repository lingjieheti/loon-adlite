# Bộ lọc quảng cáo gọn nhẹ cho Loon trên iPhone và iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Tiếng Việt** · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

Tôi chia sẻ liên kết đăng ký dùng chung trên iPhone và iPad cho những ai thường dùng JD, Taobao hay Meituan, kể cả du học sinh ở Trung Quốc. Loon chặn yêu cầu ngay trên thiết bị khi tên máy chủ khớp hoàn toàn với một tên miền quảng cáo trong danh sách. Để lọc thêm một số quảng cáo nhúng trong ứng dụng, bạn có thể bật quy tắc viết lại trên thiết bị cho những yêu cầu cụ thể.

## Cài đặt

**[Cài bộ lọc tất cả trong một](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [Địa chỉ đăng ký](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Mở liên kết cài đặt trong Safari rồi xác nhận nhập vào Loon. Bạn cũng có thể dán địa chỉ đăng ký vào Configuration → Plugins → ＋. Lọc theo tên miền không cần chứng chỉ. Tiện ích xử lý ngay trên thiết bị, không tải mã lệnh từ xa và không thu thập dữ liệu sử dụng.

Nếu đã đăng ký bản Suite, bạn chỉ cần làm mới đăng ký hiện tại. Nếu từng dùng tiện ích chặn quảng cáo khác của dự án này, hãy tắt mục cũ sau khi bật bản tất cả trong một để tránh áp dụng quy tắc hai lần.

## Quảng cáo trong nội dung ứng dụng

Để lọc một số quảng cáo trong bài viết của tài khoản chính thức WeChat hoặc trên trang chủ Bilibili, hãy dùng Loon 3.5.1 (bản dựng 978) trở lên. Bật quy tắc viết lại và giải mã HTTPS cho các máy chủ được liệt kê, rồi đặt thiết bị tin cậy chứng chỉ Loon do bạn tự tạo. Những yêu cầu khác tới cùng máy chủ cũng có thể được giải mã, làm tăng thời gian kết nối và xử lý. [Hướng dẫn giải mã HTTPS của Loon](https://nsloon.app/docs/MitM/)

Quy tắc cho bảng tin Douyin đã được thử với dữ liệu mẫu. Hiệu quả trên phiên bản ứng dụng hiện tại vẫn cần kiểm tra trên thiết bị. Đoạn tài trợ ghi sẵn trong video vẫn phát.

## Công cụ tùy chọn cho Safari

Công cụ dành cho trang web YouTube thử bấm nút Bỏ qua quảng cáo khi nút chính thức xuất hiện. Một công cụ riêng có thể ẩn một số vị trí quảng cáo trên Pornhub. [Mở đoạn mã cho YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Mở đoạn mã cho Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

## Cập nhật

Mỗi ngày, GitHub đối chiếu các tên miền quảng cáo với nguồn gốc của danh sách và kiểm tra bảo mật trong mỗi lần đối chiếu. Khi danh sách tên miền đã duyệt thay đổi, bản cập nhật chỉ được tự động đăng tại địa chỉ đăng ký cũ sau khi vượt qua kiểm tra bảo mật và toàn bộ kiểm thử. Nguồn của các quy tắc lọc quảng cáo trong ứng dụng như Bilibili và JD cũng được đối chiếu hằng ngày. Mọi thay đổi đối với các quy tắc này đều được đánh giá bảo mật riêng trước khi phát hành.

Địa chỉ đăng ký theo nhánh `main`. Bạn có thể đặt Loon kiểm tra tài nguyên bên ngoài hằng ngày. Để quay lại bản cũ, thay `main` trong địa chỉ bằng mã băm đầy đủ của lần sửa đổi mong muốn. [Lịch sử thay đổi](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Phạm vi lọc theo ứng dụng (tiếng Trung)](COVERAGE.md) · [Nguồn tham khảo theo tính năng (tiếng Trung)](SOURCES.md) · [Kiểm thử hồi quy ngoại tuyến](tests/) · [Ủng hộ tác giả (tiếng Anh)](SPONSOR.en.md) · [Kiểm tra bảo mật (tiếng Trung)](SECURITY-AUDIT.md)
