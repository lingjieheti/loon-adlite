# กฎกรองโฆษณา Loon สำหรับ iPhone และ iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · **ไทย** · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

ทำกฎชุดนี้ไว้ใช้กับ iPhone และ iPad ของตัวเอง และนำมาแบ่งปันให้คนที่ใช้แอปจีนในชีวิตประจำวัน รวมถึงนักเรียน นักศึกษา และคนที่มาทำงานหรืออาศัยอยู่ในจีน กฎช่วยกรองโฆษณาบางส่วนที่แสดงตอนเปิดแอปหรือระหว่างเลื่อนฟีด เช่น เวลาใช้ JD หรือ Taobao ซื้อของ หรือใช้ Meituan สั่งอาหาร ปลั๊กอิน Loon ทั้งสามรุ่นทำงานบนอุปกรณ์ของคุณ ไม่เก็บข้อมูลการใช้งานและไม่เรียกใช้สคริปต์จากภายนอก

## เลือกรุ่นและติดตั้ง

เปิดลิงก์ติดตั้งใน Safari แล้วกดยืนยันการนำเข้าใน Loon หรือคัดลอกลิงก์สมัครรับกฎไปวางใน Loon ที่เมนู Configuration → Plugins → ＋

- **Lite** เหมาะสำหรับเริ่มใช้ บล็อกคำขอเมื่อชื่อโฮสต์ปลายทางตรงกับชื่อในรายการโฮสต์โฆษณาทุกตัวอักษร ใช้ได้โดยไม่ต้องถอดรหัส HTTPS หรือติดตั้งใบรับรอง [ติดตั้ง Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [ลิงก์สมัครรับกฎ](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** ใช้เสริม Lite เพื่อกรองโฆษณาบางส่วนในบทความจากบัญชีทางการของ WeChat รวมถึงโฆษณาบนฟีดหน้าแรกและตอนเปิดแอป Bilibili [ติดตั้ง Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [ลิงก์สมัครรับกฎ](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite** รวมกฎของ Lite และ Inline พร้อมกฎเฉพาะสำหรับแอปอย่าง JD, Taobao, Meituan และ Douyin ถ้าเลือก Suite ให้ปิดอีกสองรุ่นเพื่อไม่ให้กฎทำงานซ้ำ กฎของ Douyin มุ่งกรองโพสต์ที่ระบุว่าเป็นโฆษณาในฟีดแนะนำ ผ่านการทดสอบด้วยข้อมูลตัวอย่างแล้ว ส่วนผลกับแอปรุ่นปัจจุบันยังต้องทดสอบบนอุปกรณ์จริง [ติดตั้ง Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [ลิงก์สมัครรับกฎ](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

กฎแก้ไขคำขอและการตอบกลับ (Rewrite) ของ Suite และ Inline ต้องใช้ Loon 3.5.1 (บิลด์ 978) ขึ้นไป ให้เปิด Rewrite เปิดการถอดรหัส HTTPS สำหรับโฮสต์ที่ระบุ และตั้งค่าให้อุปกรณ์เชื่อถือใบรับรอง Loon ของคุณ คำขออื่นที่ส่งไปยังโฮสต์เดียวกันก็อาจถูกถอดรหัสด้วย การสร้างการเชื่อมต่อ TLS และการประมวลผลข้อมูลตอบกลับใช้เวลาเพิ่มขึ้นมากน้อยต่างกันตามอุปกรณ์ เครือข่าย และแอป [คู่มือการถอดรหัสของ Loon](https://nsloon.app/docs/MitM/)

## ตัวช่วยเสริมใน Safari

Lite และ Suite กรองคำขอโฆษณาบนเว็บบางส่วนอยู่แล้ว เช่น คำขอประมูลโฆษณาของ PubMatic และ Criteo หากต้องการใช้ตัวช่วยด้านล่าง ให้เปิดใช้ส่วนขยาย Userscripts ใน Safari เปิดลิงก์สคริปต์ แล้วเลือกติดตั้งจากเมนูส่วนขยาย จากนั้นอนุญาตให้ทำงานบนเว็บไซต์ที่ต้องการ [ดาวน์โหลด Userscripts](https://apps.apple.com/app/id1463298887)

- **YouTube บนเว็บ** ซ่อนช่องโฆษณาบางส่วนในหน้าแรกและผลการค้นหา และพยายามกดปุ่ม “ข้ามโฆษณา” เมื่อเครื่องเล่นอนุญาตให้กด ตัวช่วยนี้ใช้กับเว็บไซต์ใน Safari เท่านั้น ช่วงแนะนำสินค้าที่ครีเอเตอร์ใส่ไว้ในวิดีโอยังเล่นตามปกติ [ติดตั้งตัวช่วย YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Pornhub บนเว็บ** ซ่อนแบนเนอร์ด้านข้างและช่องโฆษณาบางตำแหน่งที่ระบุได้ในหน้าดูวิดีโอบนมือถือ โฆษณาที่รวมอยู่ในสตรีมเดียวกับวิดีโอยังอาจเล่นอยู่ [ติดตั้งตัวช่วยสำหรับเว็บไซต์](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **เช็กอินและรับคูปอง** คู่มือรวมทางเข้าเช็กอินรับแต้ม JD Beans และเช็กอินรายวันของ SMZDM (什么值得买) พร้อมทางไปรับคูปองของ JD, Taobao และ Douyin คุณเลือกคูปองทั่วไปของ JD หรือคูปองร้านค้าบน Taobao แล้วให้ตัวช่วยลองรับคูปองขณะเปิดหน้าเว็บใน Safari ได้ ส่วนการเช็กอินบน Taobao และการรับสิทธิพิเศษของ Douyin ให้ดำเนินการในหน้ากิจกรรมทางการหรือในแอป [ติดตั้งตัวช่วยเช็กอิน](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js) · [คู่มือเช็กอินและรับคูปอง (ภาษาจีน)](checkin/README.md)

## อัปเดตและย้อนกลับไปใช้รุ่นก่อน

ลิงก์สมัครรับกฎของแต่ละรุ่นติดตามสาขา `main` ของโครงการ กฎจะผ่านการตรวจสอบอัตโนมัติบน GitHub ก่อนเผยแพร่ คุณตั้งให้ Loon ตรวจหาอัปเดตของทรัพยากรภายนอกวันละครั้งได้ โดยแอปเป็นผู้กำหนดเวลาที่ตรวจจริง หากคัดลอกไฟล์ผ่าน USB ให้เปลี่ยนไฟล์เองเมื่อมีรุ่นใหม่

หากต้องการกลับไปใช้กฎรุ่นก่อน ให้เปลี่ยน `main` ในลิงก์สมัครรับกฎเป็นรหัสคอมมิตแบบเต็มของรุ่นที่ต้องการ นำเข้าลิงก์นั้น แล้วปิดรายการสมัครรับกฎเดิม [ดูประวัติการแก้ไข](https://github.com/lingjieheti/loon-adlite/commits/main/)

[แอปที่รองรับและข้อจำกัด (ภาษาจีน)](COVERAGE.md) · [สนับสนุนโครงการ (ภาษาอังกฤษ)](SPONSOR.en.md)
