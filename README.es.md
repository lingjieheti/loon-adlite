# Mi filtro de anuncios todo en uno para Loon

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · **Español** · [العربية](README.ar.md)

Uso este complemento en mi iPhone y mi iPad. Lo comparto con quienes usan aplicaciones chinas a diario, incluidos los estudiantes internacionales que viven en China. Filtra algunos anuncios que aparecen al abrir JD, Taobao y Meituan, y bloquea solicitudes de sitios web a servidores de publicidad conocidos.

## Instalación

**[Instalar el complemento todo en uno](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [Dirección de suscripción](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Abre el enlace en Safari y confirma la importación en Loon. También puedes pegar la dirección de suscripción en Configuration → Plugins → ＋. El filtrado por nombre de host funciona sin certificado. El complemento procesa el tráfico en tu dispositivo, sin cargar scripts remotos ni recopilar datos de uso.

Si ya tienes una suscripción a Suite, basta con actualizarla. Si usabas otro complemento de este proyecto para bloquear anuncios, desactiva la entrada anterior después de activar el complemento todo en uno para evitar que se dupliquen las reglas.

## Anuncios dentro de las aplicaciones

Para filtrar algunos anuncios en artículos de cuentas oficiales de WeChat o en el inicio de Bilibili, usa Loon 3.5.1 (compilación 978) o posterior. Activa la reescritura y el descifrado HTTPS para los hosts indicados y marca tu propio certificado de Loon como de confianza en el dispositivo. También pueden descifrarse otras solicitudes a esos hosts. Establecer la conexión y procesar las respuestas lleva más tiempo. [Guía de descifrado de Loon](https://nsloon.app/docs/MitM/)

Las reglas para las recomendaciones de Douyin se han probado con muestras de respuestas. Aún falta comprobar su efecto en un dispositivo con la versión actual de la aplicación. Los segmentos patrocinados que forman parte del vídeo se siguen reproduciendo.

## Herramientas opcionales para Safari

En la web de YouTube, un script intenta pulsar el botón oficial para saltar el anuncio cuando aparece. Otro permite ocultar algunos espacios publicitarios en Pornhub. [Instalar el script de YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Instalar el script de Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

La guía explica cómo registrar la visita diaria en JD y SMZDM y cómo solicitar cupones de JD o de tiendas de Taobao que hayas elegido. Las promociones de Douyin se gestionan en la página oficial de cada actividad. [Guía de recompensas y cupones (en chino)](checkin/README.md)

## Actualizaciones

GitHub comprueba cada semana una selección de dominios publicitarios. Si la lista cambia y supera las pruebas, la actualización se publica automáticamente en la misma dirección de suscripción. Las reglas para anuncios integrados en aplicaciones como Bilibili y JD se revisan por separado.

La suscripción sigue la rama `main`. Puedes configurar Loon para que compruebe los recursos externos a diario. Para volver a una versión anterior, sustituye `main` en la dirección de suscripción por el hash completo del commit que quieras. [Historial de versiones](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Cobertura y límites por aplicación (en chino)](COVERAGE.md) · [Fuentes por función (en chino)](SOURCES.md) · [Pruebas de regresión sin conexión](tests/) · [Apoyar mi trabajo (en inglés)](SPONSOR.en.md) · [Auditoría de seguridad (en chino)](SECURITY-AUDIT.md)
