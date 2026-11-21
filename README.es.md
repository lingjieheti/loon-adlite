# Mis filtros de publicidad de Loon para iPhone y iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · **Español** · [العربية](README.ar.md)

Uso estos filtros en mi iPhone y mi iPad para reducir la publicidad en aplicaciones de uso diario en China continental. Si vives, estudias o trabajas allí, quizá uses JD (京东) y Taobao (淘宝) para comprar o Meituan (美团) para pedir comida. Según la aplicación, los filtros bloquean algunos anuncios al abrirla o al recorrer las recomendaciones.

## Elegir e instalar un filtro

Si es la primera vez que usas Loon, te recomiendo **Lite**. Abre el enlace de instalación en Safari y confirma la importación en Loon. También puedes pegar la URL de suscripción en Configuration → Plugins → ＋ dentro de Loon.

- **Lite** bloquea las solicitudes a 43 nombres de host concretos que se utilizan para publicidad. Funciona sin certificado ni descifrado HTTPS. [Instalar Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [URL de suscripción](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** complementa Lite. Filtra algunos anuncios en los artículos de las cuentas oficiales de WeChat, en la página de inicio de Bilibili y al abrir Bilibili. [Instalar Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [URL de suscripción](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite** reúne Lite e Inline y añade reglas para JD, Taobao, Meituan y Douyin. Si usas Suite, desactiva las otras dos ediciones para evitar duplicados. En Douyin, las reglas buscan recomendaciones marcadas como publicidad. Se han probado con respuestas de ejemplo y aún falta comprobar su efecto en la aplicación actual en un dispositivo. [Instalar Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [URL de suscripción](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

## Privacidad y rendimiento

Las tres ediciones filtran el tráfico en tu dispositivo, sin ejecutar scripts remotos ni recopilar datos de uso. Las reglas de reescritura de Suite e Inline requieren Loon 3.5.1 (compilación 978) o posterior. Activa la reescritura y el descifrado HTTPS para los hosts indicados y configura tu dispositivo para que confíe en el certificado generado por tu propia instalación de Loon. También se pueden descifrar otras solicitudes HTTPS a esos mismos hosts. El tiempo de procesamiento depende del dispositivo, la red y la aplicación. [Guía de descifrado de Loon](https://nsloon.app/docs/MitM/)

## En Safari

Lite y Suite también bloquean algunas solicitudes de publicidad en páginas web, incluidas las de subastas de PubMatic y Criteo. Para añadir un script opcional, activa la extensión Userscripts en Safari, abre el enlace del script y selecciona la opción de instalación en el menú de la extensión. Permite que se ejecute en el sitio correspondiente y vuelve a cargar la página.

- **YouTube**. En la web, el script oculta algunos espacios publicitarios del inicio y de los resultados de búsqueda. También intenta pulsar el botón para saltar el anuncio cuando el reproductor lo permite. La aplicación de YouTube y los patrocinios grabados por el creador quedan fuera de su alcance. [Instalar el script de YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Pornhub**. El script oculta algunos anuncios de la barra lateral y espacios publicitarios de la página de reproducción para móviles. Los anuncios integrados en el propio vídeo pueden seguir reproduciéndose. [Instalar el script de Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **JD y SMZDM (什么值得买)**. Si has iniciado sesión y abres la página correspondiente en Safari, un script intenta pulsar el botón de recompensa diaria. También puedes añadir un recordatorio de JD en Loon. [Configurar las recompensas diarias (en chino)](checkin/README.md)

## Actualizaciones y versiones anteriores

Las suscripciones siguen la edición publicada en `main`. Puedes configurar Loon para que revise los recursos externos a diario. La aplicación decide la hora exacta. Los archivos copiados por USB se sustituyen manualmente. Para recuperar una versión anterior, sustituye `main` en la URL de suscripción por el identificador completo del commit que quieras, importa esa URL y desactiva la entrada anterior. [Historial de versiones](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Cobertura y límites por aplicación (en chino)](COVERAGE.md) · [Apoyar mi trabajo (en inglés)](SPONSOR.en.md)
