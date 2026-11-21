# Mon filtre publicitaire tout-en-un pour Loon

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · **Français** · [Español](README.es.md) · [العربية](README.ar.md)

J’utilise ce module sur iPhone et iPad. Je le partage avec les personnes qui utilisent couramment des applications chinoises, y compris celles qui étudient en Chine. Il cible certaines publicités au lancement de JD, Taobao et Meituan et bloque les requêtes de sites web vers des serveurs publicitaires connus.

## Installation

**[Installer le module tout-en-un](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [Adresse d’abonnement](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

Ouvrez le lien dans Safari et confirmez l’importation dans Loon. Vous pouvez aussi coller l’adresse d’abonnement dans Configuration → Plugins → ＋. Le filtrage par nom d’hôte fonctionne sans certificat. Le module traite le trafic sur votre appareil, sans charger de scripts distants ni collecter de données d’utilisation.

Si vous utilisez déjà l’abonnement Suite, il suffit de l’actualiser. Si vous utilisiez un autre module de blocage publicitaire de ce projet, désactivez son entrée après avoir activé le module tout-en-un pour éviter les doublons.

## Publicités intégrées aux applications

Pour filtrer certaines publicités dans les articles des comptes officiels WeChat ou dans le fil d’accueil de Bilibili, utilisez Loon 3.5.1 (build 978) ou ultérieur. Activez la réécriture et le déchiffrement HTTPS pour les hôtes indiqués, puis déclarez votre propre certificat Loon comme fiable sur l’appareil. D’autres requêtes vers ces hôtes peuvent aussi être déchiffrées. La connexion et le traitement des réponses prennent alors plus de temps. [Guide du déchiffrement dans Loon](https://nsloon.app/docs/MitM/)

Les règles du fil de recommandations de Douyin ont été testées sur des exemples de réponses. Leur effet reste à vérifier sur appareil avec la version actuelle. Les séquences sponsorisées intégrées au montage des vidéos restent visibles.

## Outils facultatifs pour Safari

Sur le site de YouTube, un script essaie de cliquer sur le bouton officiel pour ignorer l’annonce dès qu’il apparaît. Un autre masque certains emplacements publicitaires sur Pornhub. [Installer le script YouTube](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Installer le script Pornhub](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

Le guide couvre les pointages quotidiens sur JD et SMZDM et la récupération des coupons JD ou des coupons de boutiques Taobao que vous choisissez. Les offres Douyin se trouvent sur la page officielle de l’opération. [Guide des récompenses et des coupons (en chinois)](checkin/README.md)

## Mises à jour

Chaque semaine, GitHub vérifie une sélection de domaines publicitaires. Si la liste change et que les tests réussissent, la mise à jour est publiée automatiquement à la même adresse d’abonnement. Les règles de filtrage au sein d’applications comme Bilibili et JD font l’objet d’une vérification distincte.

L’abonnement suit la branche `main`. Vous pouvez régler Loon pour vérifier les ressources externes chaque jour. Pour revenir à une version antérieure, remplacez `main` dans l’adresse par le hachage complet du commit voulu. [Historique des versions](https://github.com/lingjieheti/loon-adlite/commits/main/)

[Détail des filtres par application (en chinois)](COVERAGE.md) · [Sources par fonctionnalité (en chinois)](SOURCES.md) · [Tests de régression hors ligne](tests/) · [Soutenir mon travail (en anglais)](SPONSOR.en.md) · [Audit de sécurité (en chinois)](SECURITY-AUDIT.md)
