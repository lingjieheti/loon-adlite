# Filter iklan Loon untuk iPhone dan iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · **Bahasa Indonesia** · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

Ini kumpulan filter Loon yang saya pakai di iPhone dan iPad. Saya membagikannya untuk pengguna aplikasi Tiongkok, termasuk mahasiswa internasional yang sehari-hari berbelanja di JD (京东) atau Taobao (淘宝) dan memesan makanan lewat Meituan (美团). Filter ini memblokir sebagian iklan yang muncul saat aplikasi dibuka atau saat Anda melihat beranda. Cakupannya berbeda di setiap aplikasi.

## Memilih dan memasang filter

Jika baru memakai Loon, mulailah dengan **Lite**. Buka tautan pemasangan di Safari pada iPhone atau iPad, lalu konfirmasikan impor di Loon. Anda juga bisa menyalin URL langganan ke menu Konfigurasi → Plugin → ＋ di Loon.

- **Lite** memblokir permintaan jika nama host tujuan sama persis dengan salah satu nama dalam daftar host iklan. Anda bisa menggunakannya tanpa memasang sertifikat atau mengaktifkan dekripsi HTTPS. [Pasang Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [URL langganan](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** bisa dipakai bersama Lite untuk menyaring iklan di artikel akun resmi WeChat, kartu iklan di beranda Bilibili, dan sebagian iklan saat Bilibili dibuka. [Pasang Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [URL langganan](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite** mencakup seluruh aturan Lite dan Inline serta aturan khusus untuk JD, Taobao, Meituan, dan Douyin (抖音). Jika memakai Suite, nonaktifkan dua versi lainnya agar aturan yang sama hanya diterapkan sekali. Aturan Douyin menyasar unggahan berlabel iklan di umpan rekomendasi. Aturan ini sudah diuji dengan data contoh dan masih perlu diverifikasi pada perangkat yang menjalankan versi Douyin saat ini. [Pasang Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [URL langganan](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Ketiga versi memproses lalu lintas langsung di perangkat, tidak menjalankan skrip jarak jauh, dan tidak mengumpulkan data penggunaan. Fitur penulisan ulang respons pada Suite dan Inline memerlukan Loon 3.5.1 (build 978) atau lebih baru. Aktifkan fitur tersebut serta dekripsi HTTPS untuk host yang tercantum, lalu atur perangkat agar memercayai sertifikat Loon milik Anda sendiri. Loon juga dapat mendekripsi permintaan lain ke host yang sama. Waktu untuk membangun koneksi TLS dan memproses respons bergantung pada perangkat, jaringan, dan aplikasi. [Panduan dekripsi HTTPS dari Loon](https://nsloon.app/docs/MitM/)

## Fitur opsional di Safari

Aktifkan ekstensi Userscripts di Safari, buka tautan skrip yang diinginkan, lalu pilih opsi pemasangan dari menu ekstensi. Izinkan ekstensi berjalan di situs terkait dan muat ulang halamannya.

- **YouTube di Safari**. Skrip menyembunyikan sebagian slot iklan di beranda dan hasil pencarian. Saat tombol Lewati Iklan di pemutar tersedia, skrip mencoba mengekliknya. Fitur ini khusus untuk situs web YouTube. Segmen sponsor yang menyatu dengan video tetap diputar. [Skrip YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Iklan web**. Lite dan Suite memblokir permintaan ke beberapa host lelang dan penayangan iklan. Skrip khusus Pornhub juga dapat menyembunyikan banner di bilah samping dan slot iklan seluler yang dapat dikenali. [Skrip Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **Check-in dan kupon**. Panduan ini memuat tautan check-in harian untuk mengumpulkan JD Beans dan check-in di SMZDM (什么值得买), serta tautan kupon JD, Taobao, dan Douyin. Di Safari, skrip opsional dapat mencoba mengambil kupon reguler JD atau kupon toko Taobao yang Anda pilih. Untuk check-in Taobao dan penawaran Douyin, gunakan halaman promo resmi atau aplikasi. [Panduan check-in dan kupon (bahasa Mandarin)](checkin/README.md)

## Pembaruan dan cara kembali ke versi lama

URL langganan mengikuti pembaruan di cabang `main`. Anda bisa mengatur Loon untuk memeriksa sumber daya eksternal setiap hari. Waktu pembaruan ditentukan oleh Loon. Jika Anda menyalin berkas lewat USB, gantilah secara manual saat memperbarui. Untuk kembali ke versi lama, ganti `main` pada URL langganan dengan hash lengkap dari commit yang dipilih, impor URL tersebut, lalu nonaktifkan entri sebelumnya. [Riwayat perubahan](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Cakupan dan batasan per aplikasi (bahasa Mandarin)](COVERAGE.md) · [Dukung proyek ini (bahasa Inggris)](SPONSOR.en.md)
