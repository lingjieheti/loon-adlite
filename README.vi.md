# Bộ lọc quảng cáo Loon cho iPhone và iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Tiếng Việt** · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

Đây là bộ lọc tôi dùng trên iPhone và iPad của mình. Tôi chia sẻ bộ lọc này cho những ai thường dùng ứng dụng Trung Quốc, chẳng hạn du học sinh mua sắm trên JD (京东), Taobao (淘宝) hay đặt đồ ăn qua Meituan (美团). Bộ lọc chặn một phần quảng cáo lúc mở ứng dụng và trong bảng tin. Phạm vi lọc tùy từng ứng dụng.

## Chọn và cài đặt

Nếu mới dùng Loon, bạn có thể bắt đầu với **Lite**. Mở liên kết cài đặt bằng Safari trên iPhone hoặc iPad rồi xác nhận nhập trong Loon. Bạn cũng có thể sao chép địa chỉ đăng ký và dán vào mục Cấu hình → Plugin → ＋ trong Loon.

- **Lite** chặn yêu cầu khi tên máy chủ khớp hoàn toàn với một mục trong danh sách máy chủ quảng cáo. Bạn không cần cài chứng chỉ hay giải mã HTTPS. [Cài Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [Địa chỉ đăng ký](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** dùng được cùng với Lite để lọc quảng cáo trong bài viết của tài khoản chính thức trên WeChat, thẻ quảng cáo ở trang chủ Bilibili và một số quảng cáo khi mở Bilibili. [Cài Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [Địa chỉ đăng ký](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite** gồm toàn bộ quy tắc của Lite và Inline, kèm quy tắc riêng cho JD, Taobao, Meituan và Douyin (抖音). Khi dùng Suite, hãy tắt hai bản còn lại để tránh áp dụng quy tắc hai lần. Quy tắc lọc bài có nhãn quảng cáo trong mục đề xuất của Douyin đã được thử với dữ liệu mẫu. Hiệu quả trên phiên bản Douyin hiện tại vẫn cần kiểm tra trên thiết bị thật. [Cài Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [Địa chỉ đăng ký](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Cả ba bản đều xử lý lưu lượng ngay trên thiết bị, không chạy mã từ xa và không thu thập dữ liệu sử dụng. Tính năng viết lại phản hồi của Suite và Inline cần Loon 3.5.1 (bản dựng 978) trở lên. Hãy bật tính năng viết lại, bật giải mã HTTPS cho các máy chủ được liệt kê và đặt thiết bị tin cậy chứng chỉ Loon của chính bạn. Các yêu cầu khác tới cùng máy chủ cũng có thể được giải mã. Thời gian thiết lập kết nối TLS và xử lý phản hồi phụ thuộc vào thiết bị, mạng và ứng dụng. [Hướng dẫn giải mã HTTPS của Loon](https://nsloon.app/docs/MitM/)

## Tiện ích tùy chọn cho Safari

Bật tiện ích Userscripts trong Safari, mở liên kết của đoạn mã muốn dùng rồi chọn cài đặt trong menu tiện ích. Cho phép tiện ích chạy trên trang tương ứng và tải lại trang.

- **YouTube trên web** có thể ẩn một số vị trí quảng cáo ở trang chủ và kết quả tìm kiếm. Khi nút bỏ qua quảng cáo của trình phát khả dụng, đoạn mã sẽ thử nhấn nút. Tính năng này chỉ hoạt động trên web. Các đoạn tài trợ đã ghép vào video vẫn phát. [Mở đoạn mã cho YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Quảng cáo trên web**. Lite và Suite chặn các yêu cầu gửi đến một số máy chủ đấu giá và phân phối quảng cáo. Trên Pornhub, bạn có thể cài thêm đoạn mã để ẩn các biểu ngữ ở thanh bên và một số vị trí quảng cáo trên giao diện di động. [Mở đoạn mã cho Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **Điểm danh và nhận mã giảm giá**. Hướng dẫn có đường dẫn điểm danh hằng ngày để nhận điểm 京豆 trên JD, điểm danh trên SMZDM (什么值得买) và tìm mã giảm giá của JD, Taobao, Douyin. Bạn có thể chọn phiếu giảm giá thông thường trên JD hoặc phiếu của cửa hàng Taobao rồi để tiện ích tương ứng thử nhận khi trang đang mở trong Safari. Hãy điểm danh Taobao và nhận ưu đãi Douyin trên trang chính thức hoặc trong ứng dụng. [Hướng dẫn điểm danh và nhận mã (tiếng Trung)](checkin/README.md)

## Cập nhật và khôi phục phiên bản cũ

Địa chỉ đăng ký lấy bản cập nhật từ nhánh `main`. Bạn có thể đặt Loon kiểm tra tài nguyên bên ngoài hằng ngày. Thời điểm làm mới do Loon quyết định. Nếu đã chép tệp qua USB, hãy tự thay tệp khi cập nhật. Để quay lại bản cũ, thay `main` trong địa chỉ đăng ký bằng mã băm đầy đủ của lần lưu (commit) bạn muốn dùng, nhập địa chỉ đó rồi tắt mục cũ. [Lịch sử thay đổi](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Phạm vi lọc theo ứng dụng (tiếng Trung)](COVERAGE.md) · [Ủng hộ tác giả (tiếng Anh)](SPONSOR.en.md)
