# قواعد حجب الإعلانات التي أستخدمها مع Loon على iPhone وiPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · **العربية**

<div dir="rtl" lang="ar">

أستخدم هذه القواعد على أجهزتي، وأشاركها مع من يعتمدون على التطبيقات الصينية في حياتهم اليومية، بمن فيهم الطلاب الدوليون والمقيمون في الصين. تحجب القواعد بعض الإعلانات التي تظهر عند فتح التطبيقات أو أثناء تصفّحها، مثل تطبيقات التسوّق JD وTaobao وتطبيق توصيل الطعام Meituan. تعالج إضافات Loon الثلاث الاتصال على جهازك، ولا تجمع بيانات الاستخدام أو تشغّل سكربتات عن بُعد.

## اختيار النسخة وتثبيتها

افتح رابط التثبيت في Safari ثم أكّد استيراد الإضافة في Loon. ويمكنك أيضاً نسخ رابط الاشتراك، وفتح قسم الإضافات (Plugins) ضمن إعدادات Loon (Configuration)، ثم الضغط على زر الإضافة (+) ولصق الرابط.

- **النسخة الخفيفة (Lite)** مناسبة للبدء. تحجب الطلبات المرسلة إلى 43 مضيفاً إعلانياً محدداً، من دون تثبيت شهادة أو فك تشفير HTTPS. [تثبيت Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [رابط الاشتراك](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **نسخة الإعلانات المضمّنة (Inline)** يمكن إضافتها إلى Lite لحجب بعض الإعلانات داخل مقالات حسابات WeChat الرسمية، وفي الصفحة الرئيسية لتطبيق Bilibili وعند فتحه. [تثبيت Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [رابط الاشتراك](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **النسخة الشاملة (Suite)** تجمع قواعد النسختين وتضيف قواعد لتطبيقات منها JD وTaobao وMeituan وDouyin. عند اختيارها عطّل النسختين الأخريين لتجنّب تكرار القواعد. تستهدف قواعد Douyin المنشورات الموسومة بأنها إعلانات في صفحة التوصيات. اختُبرت هذه القواعد على عيّنات، وما زال أداؤها في الإصدار الحالي من التطبيق بحاجة إلى اختبار على جهاز فعلي. [تثبيت Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [رابط الاشتراك](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

تتطلّب قواعد إعادة الكتابة في Inline وSuite إصدار Loon 3.5.1 (البناء 978) أو أحدث. فعّل إعادة الكتابة وفك تشفير HTTPS للمضيفين المحدّدين وامنح الثقة لشهادة Loon الخاصة بك على الجهاز. يمكن أن يشمل فك التشفير طلبات أخرى إلى المضيف نفسه. يختلف الوقت الإضافي الذي يستغرقه إنشاء اتصال TLS ومعالجة الاستجابة باختلاف الجهاز والشبكة والتطبيق. [دليل Loon لفك التشفير](https://nsloon.app/docs/MitM/)

## أدوات اختيارية في Safari

تمنع Lite وSuite بعض طلبات إعلانات الويب، ومنها طلبات مزادات الإعلانات على PubMatic وCriteo. لاستخدام إحدى الأدوات التالية، فعّل إضافة Userscripts في Safari، وافتح رابط السكربت، ثم ثبّته من قائمة الإضافة واسمح بتشغيله على الموقع المطلوب. [تنزيل Userscripts](https://apps.apple.com/app/id1463298887)

- **يوتيوب**. تخفي الأداة بعض الإعلانات في الصفحة الرئيسية ونتائج البحث على الموقع، وتحاول الضغط على زر «تخطّي الإعلان» حين يصبح متاحاً. يقتصر عملها على Safari ولا يشمل تطبيق YouTube. وتبقى مقاطع الرعاية المسجّلة ضمن الفيديو. [تثبيت أداة YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **موقع Pornhub**. تخفي الأداة بعض اللافتات الجانبية والمواضع الإعلانية المعروفة في صفحة المشغّل على الهاتف. قد تظل الإعلانات المدمجة في بثّ الفيديو ظاهرة. [تثبيت أداة الموقع](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **المكافآت اليومية في JD وSMZDM (什么值得买)**. بعد تسجيل الدخول افتح صفحة المكافآت عبر الرابط المخصّص للخدمة. عندها تحاول الأداة الضغط على زر المطالبة بالمكافأة اليومية. يتوفّر أيضاً تذكير اختياري في Loon لخدمة JD. [تثبيت الأداة](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/checkin/daily.user.js) · [روابط الصفحات وإعداد التذكير (بالصينية)](checkin/README.md)

## التحديث والعودة إلى إصدار سابق

يتتبّع كل رابط اشتراك نسخته على فرع `main`. تمرّ القواعد بفحوص آلية على GitHub قبل نشرها. يمكنك ضبط Loon ليتحقّق من تحديثات الموارد الخارجية يومياً. يحدّد التطبيق وقت التحديث الفعلي، أمّا الملفات المنسوخة عبر USB فتحتاج إلى استبدال يدوي.

للعودة إلى نسخة سابقة، استبدل `main` في رابط الاشتراك بالمعرّف الكامل للتغيير المطلوب على GitHub، ثم استورد الرابط وعطّل الاشتراك السابق. [سجلّ التغييرات](https://github.com/lingjieheti/loon-adlite/commits/main/)

[التطبيقات المشمولة والقيود (بالصينية)](COVERAGE.md) · [دعم المشروع (بالإنجليزية)](SPONSOR.en.md)

</div>
