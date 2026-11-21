# Filter iklan ringan untuk Loon di iPhone dan iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · **Bahasa Indonesia** · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

Saya membagikan satu langganan yang saya pakai di iPhone dan iPad untuk pengguna aplikasi Tiongkok seperti JD, Taobao, dan Meituan, termasuk mahasiswa asing di Tiongkok. Loon memblokir permintaan di perangkat jika nama host sama persis dengan salah satu domain iklan dalam daftar. Untuk menyaring sebagian iklan di dalam aplikasi, Anda juga bisa mengaktifkan aturan penulisan ulang lokal yang berlaku pada permintaan tertentu.

## Pemasangan

**[Pasang plugin serbaguna](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [Alamat langganan](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Buka tautan pemasangan di Safari lalu konfirmasikan impor di Loon. Anda juga bisa menempelkan alamat langganan di Configuration → Plugins → ＋. Pemblokiran berdasarkan nama host berfungsi tanpa sertifikat. Plugin memproses lalu lintas di perangkat, tidak memuat skrip jarak jauh, dan tidak mengumpulkan data penggunaan.

Jika sudah berlangganan Suite, cukup segarkan langganan tersebut. Jika sebelumnya memakai plugin pemblokir iklan lain dari proyek ini, nonaktifkan entri lama setelah mengaktifkan plugin serbaguna agar aturan tidak diterapkan dua kali.

## Iklan di dalam aplikasi

Untuk menyaring sebagian iklan di artikel akun resmi WeChat atau beranda Bilibili, gunakan Loon 3.5.1 (build 978) atau yang lebih baru. Aktifkan penulisan ulang dan dekripsi HTTPS untuk host yang terdaftar, lalu percayai sertifikat Loon yang Anda buat sendiri di perangkat. Permintaan lain ke host yang sama juga dapat didekripsi. Proses koneksi dan pengolahan respons membutuhkan waktu tambahan. [Panduan dekripsi HTTPS dari Loon](https://nsloon.app/docs/MitM/)

Aturan untuk beranda rekomendasi Douyin telah diuji dengan sampel respons. Hasil pada versi aplikasi saat ini masih perlu diperiksa langsung di perangkat. Segmen sponsor yang direkam di dalam video tetap diputar.

## Alat opsional untuk Safari

Alat untuk situs YouTube mencoba menekan tombol Lewati Iklan resmi saat tombolnya muncul. Alat terpisah dapat menyembunyikan beberapa slot iklan di Pornhub. [Skrip YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Skrip Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

## Pembaruan

GitHub mencocokkan daftar host iklan dengan sumbernya setiap hari dan menjalankan audit keamanan pada setiap pemeriksaan. Perubahan pada daftar host yang disetujui otomatis terbit di URL langganan yang sama setelah lolos audit dan seluruh pengujian. Sumber aturan untuk iklan dalam aplikasi seperti Bilibili dan JD juga diperiksa setiap hari. Perubahan pada aturan tersebut menjalani peninjauan keamanan tersendiri sebelum diterbitkan.

Alamat langganan mengikuti cabang `main`. Atur Loon untuk memeriksa sumber daya eksternal setiap hari. Untuk kembali ke versi lama, ganti `main` pada alamat langganan dengan hash lengkap commit yang diinginkan. [Riwayat perubahan](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Cakupan dan batasan per aplikasi (bahasa Mandarin)](COVERAGE.md) · [Sumber tiap fitur (bahasa Mandarin)](SOURCES.md) · [Uji regresi luring](tests/) · [Dukung proyek ini (bahasa Inggris)](SPONSOR.en.md) · [Audit keamanan (bahasa Mandarin)](SECURITY-AUDIT.md)
