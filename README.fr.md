# Mes filtres Loon pour iPhone et iPad

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · **Français** · [Español](README.es.md) · [العربية](README.ar.md)

J’utilise ces filtres sur mon iPhone et mon iPad pour limiter la publicité dans les applications du quotidien en Chine continentale. Si vous y étudiez ou y travaillez, vous connaissez peut-être JD (京东) et Taobao (淘宝) pour les achats, ou Meituan (美团) pour les livraisons de repas. Selon l’application, les filtres bloquent certaines publicités au démarrage ou dans le fil de recommandations.

## Choisir et installer un filtre

Pour commencer, je conseille **Lite**. Ouvrez le lien d’installation dans Safari, puis confirmez l’importation dans Loon. Vous pouvez aussi copier l’URL d’abonnement dans Loon, sous Configuration → Plugins → ＋.

- **Lite** bloque les requêtes vers 43 noms d’hôte précis utilisés pour la publicité. Aucun certificat ni déchiffrement HTTPS n’est nécessaire. [Installer Lite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [URL d’abonnement](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline** complète Lite en filtrant certaines publicités dans les articles des comptes officiels WeChat, sur la page d’accueil de Bilibili et au lancement de Bilibili. [Installer Inline](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [URL d’abonnement](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite** regroupe Lite et Inline et ajoute des règles pour JD, Taobao, Meituan et Douyin. Si vous activez Suite, désactivez Lite et Inline pour éviter les doublons. Les règles Douyin ciblent les recommandations signalées comme publicitaires. Elles ont été testées sur des exemples de réponses, mais leur efficacité dans la version actuelle de l’application reste à vérifier sur un appareil. [Installer Suite](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [URL d’abonnement](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

## Confidentialité et performances

Les trois éditions traitent le trafic sur votre appareil, sans exécuter de scripts distants ni recueillir de données d’utilisation. Dans Suite et Inline, les règles de réécriture nécessitent Loon 3.5.1 (build 978) ou une version ultérieure. Activez la réécriture et le déchiffrement HTTPS pour les hôtes indiqués, puis autorisez le certificat créé par votre propre installation de Loon. Les autres requêtes HTTPS vers ces mêmes hôtes peuvent aussi être déchiffrées. Le temps de traitement dépend de l’appareil, du réseau et de l’application. [Guide du déchiffrement dans Loon](https://nsloon.app/docs/MitM/)

## Dans Safari

Lite et Suite bloquent aussi certaines requêtes publicitaires sur le Web, notamment des enchères PubMatic et Criteo. Pour ajouter un script facultatif, activez l’extension Userscripts dans Safari, ouvrez le lien du script, puis choisissez de l’installer dans le menu de l’extension. Autorisez son exécution sur le site concerné et rechargez la page.

- **YouTube**. Sur le site, le script masque certains emplacements publicitaires de l’accueil et des résultats de recherche. Il tente de cliquer sur le bouton permettant de passer l’annonce dès que celui-ci devient disponible. L’application YouTube et les séquences de parrainage intégrées par le créateur restent hors de sa portée. [Installer le script YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **Pornhub**. Le script masque certaines bannières latérales et certains emplacements publicitaires de la page de lecture mobile. Les publicités intégrées au flux vidéo peuvent toujours être diffusées. [Installer le script Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **JD et SMZDM (什么值得买)**. Une fois que vous avez ouvert la page dédiée dans Safari et que vous êtes connecté, un script peut cliquer sur le bouton de récompense quotidienne. Un rappel JD est aussi disponible pour Loon. [Configurer les récompenses quotidiennes (en chinois)](checkin/README.md)

## Mises à jour et retour à une version antérieure

Pour suivre la version publiée sur `main`, demandez à Loon de vérifier les ressources externes chaque jour. Loon détermine l’heure de la vérification. Les fichiers copiés par USB se remplacent manuellement. Pour retrouver une ancienne version, remplacez `main` dans l’URL d’abonnement par l’identifiant complet du commit souhaité, importez la nouvelle URL et désactivez l’entrée précédente. [Historique des versions](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Détail des filtres par application (en chinois)](COVERAGE.md) · [Soutenir mon travail (en anglais)](SPONSOR.en.md)
