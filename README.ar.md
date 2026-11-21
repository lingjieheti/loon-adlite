# إضافة Loon الشاملة لحجب الإعلانات على iPhone وiPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · **العربية**

<div dir="rtl" lang="ar">

أستخدم هذه الإضافة على أجهزتي وأشاركها مع من يستخدمون التطبيقات الصينية بانتظام، بمن فيهم الطلاب الدوليون المقيمون في الصين. تستهدف بعض الإعلانات التي تظهر عند فتح JD وTaobao وMeituan، وتحجب طلبات مواقع الويب المتجهة إلى خوادم إعلانية معروفة.

## التثبيت

**[تثبيت الإضافة الشاملة](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [رابط الاشتراك](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

افتح رابط التثبيت في Safari وأكّد الاستيراد في Loon. يمكنك أيضاً لصق رابط الاشتراك في Configuration → Plugins → ＋. يعمل الحجب بحسب اسم المضيف من دون شهادة. تُعالَج الطلبات على جهازك، ولا تحمّل الإضافة سكربتات عن بُعد ولا تجمع بيانات الاستخدام.

إذا كنت مشتركاً في نسخة Suite، يكفي تحديث اشتراكك الحالي. وإذا كنت تستخدم إضافة أخرى من هذا المشروع لحجب الإعلانات، فعطّل الإدخال القديم بعد تفعيل الإضافة الشاملة حتى لا تتكرر القواعد.

## الإعلانات المضمّنة في التطبيقات

لتصفية بعض الإعلانات داخل مقالات حسابات WeChat الرسمية أو في الصفحة الرئيسية لتطبيق Bilibili، استخدم Loon 3.5.1 (البناء 978) أو أحدث. فعّل إعادة الكتابة وفك تشفير HTTPS للمضيفين المذكورين، وامنح الثقة على جهازك لشهادة Loon التي أنشأتها بنفسك. قد تُفكّ أيضاً شيفرة طلبات أخرى للمضيف نفسه، ويستغرق الاتصال ومعالجة الردود وقتاً إضافياً. [دليل Loon لفك التشفير](https://nsloon.app/docs/MitM/)

اختُبرت قواعد موجز التوصيات في Douyin على عيّنات من الردود. ما زال أثرها في الإصدار الحالي من التطبيق بحاجة إلى اختبار فعلي على جهاز. وتبقى مقاطع الرعاية المدمجة في الفيديو ضمن التسجيل.

## أدوات اختيارية في Safari

تحاول أداة موقع YouTube الضغط على زر تخطّي الإعلان الرسمي عند ظهوره. ويمكن لأداة منفصلة إخفاء بعض المساحات الإعلانية على موقع Pornhub. [تثبيت أداة YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [تثبيت أداة الموقع](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js) · [تنزيل Userscripts](https://apps.apple.com/app/id1463298887)

يشرح الدليل تسجيل الحضور اليومي في JD وSMZDM والحصول على قسائم تختارها في JD أو متاجر Taobao. ولعروض Douyin استخدم الصفحة الرسمية للفعالية. [دليل المكافآت والقسائم (بالصينية)](checkin/README.md) · [تثبيت الأداة](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js)

## التحديثات

يتابع الاشتراك فرع `main`. يمكنك ضبط Loon ليتحقق يومياً من تحديثات الموارد الخارجية. وللعودة إلى إصدار سابق، استبدل `main` في رابط الاشتراك بالمعرّف الكامل للتغيير المطلوب. [سجلّ التغييرات](https://github.com/lingjieheti/loon-adlite/commits/main/)

[التطبيقات المشمولة والقيود (بالصينية)](COVERAGE.md) · [مصادر كل ميزة (بالصينية)](SOURCES.md) · [اختبارات الانحدار دون اتصال](tests/) · [دعم المشروع (بالإنجليزية)](SPONSOR.en.md)

</div>
