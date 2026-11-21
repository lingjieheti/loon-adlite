# iPhone과 iPad에서 쓰는 Loon 광고 필터

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · **한국어** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

제가 iPhone과 iPad에서 쓰는 Loon 광고 필터입니다. 중국에서 공부하거나 생활하면서 징둥(京东)과 타오바오(淘宝)로 장을 보고 메이퇀(美团)으로 음식을 주문하는 분들과 공유합니다. 앱을 열 때나 피드를 볼 때 나오는 광고를 일부 차단하며, 적용 범위는 앱마다 다릅니다.

## 버전 선택과 설치

처음이라면 **Lite**로 시작하세요. iPhone 또는 iPad의 Safari에서 설치 링크를 열고 Loon에서 가져오기를 확인하세요. 구독 주소를 복사해 Loon의 구성 → 플러그인 → ＋에 붙여 넣어도 됩니다.

- **Lite**는 요청의 호스트 이름이 광고 목록의 항목과 정확히 일치할 때 차단합니다. 인증서 설치나 HTTPS 복호화가 필요 없습니다. [Lite 설치](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdLite.lpx) · [구독 주소](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdLite.lpx)
- **Inline**은 Lite와 함께 쓸 수 있습니다. 위챗 공식 계정 글의 광고, 빌리빌리 홈 피드의 광고 카드, 앱 실행 시 나오는 빌리빌리 광고 일부를 걸러냅니다. [Inline 설치](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-InlineAds.lpx) · [구독 주소](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-InlineAds.lpx)
- **Suite**에는 Lite와 Inline의 모든 규칙에 더해 징둥, 타오바오, 메이퇀, 더우인(抖音) 전용 규칙이 들어 있습니다. Suite를 사용하면 중복 적용을 피하도록 나머지 두 버전은 꺼 주세요. 더우인 추천 피드의 광고 표시는 샘플로 테스트했으며, 현행 앱에서의 차단 효과는 실기기 검증이 필요합니다. [Suite 설치](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx) · [구독 주소](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

세 버전 모두 기기 안에서 트래픽을 처리하며 원격 스크립트를 실행하거나 사용 기록을 수집하지 않습니다. Suite와 Inline의 응답 재작성 기능에는 Loon 3.5.1(빌드 978) 이상이 필요합니다. 재작성과 지정 호스트의 HTTPS 복호화를 켜고 기기에서 본인의 Loon 인증서를 신뢰하도록 설정하세요. 같은 호스트로 가는 다른 요청도 복호화될 수 있습니다. TLS 연결과 응답 처리에 드는 시간은 기기와 네트워크, 앱에 따라 달라집니다. [Loon의 HTTPS 복호화 안내](https://nsloon.app/docs/MitM/)

## Safari에서 선택해서 쓰는 기능

Safari에서 Userscripts 확장 프로그램을 켠 뒤 원하는 스크립트 링크를 열고 확장 메뉴에서 설치하세요. 해당 사이트에서 실행을 허용하고 페이지를 새로 고치면 됩니다.

- **YouTube 웹**에서는 홈 화면과 검색 결과의 광고 일부를 숨기고, 플레이어에 ‘광고 건너뛰기’ 버튼이 활성화되면 클릭을 시도합니다. YouTube 앱에는 적용되지 않으며 영상에 편집해 넣은 협찬 장면은 그대로 재생됩니다. [YouTube 스크립트](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js)
- **웹 광고**는 Lite와 Suite가 일부 광고 입찰 및 송출 요청을 차단합니다. Pornhub용 Safari 스크립트를 추가하면 식별 가능한 사이드바 배너와 모바일 광고 영역도 숨길 수 있습니다. [Pornhub 스크립트](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)
- **출석 체크와 쿠폰**. 징둥 포인트(京豆)와 SMZDM(什么值得买)의 일일 출석 체크, 징둥·타오바오·더우인 쿠폰을 한곳에서 찾을 수 있습니다. 징둥 일반 쿠폰이나 타오바오 상점 쿠폰을 직접 선택하고 Safari에서 열면 해당 도우미가 수령을 시도합니다. 타오바오 출석 체크와 더우인 혜택은 공식 이벤트 페이지나 앱에서 확인하세요. [출석 체크 및 쿠폰 안내(중국어)](checkin/README.md)

## 업데이트와 이전 버전 복원

구독 주소는 선택한 버전의 `main` 브랜치를 따릅니다. Loon에서 외부 리소스를 매일 확인하도록 설정할 수 있으며, 실제 갱신 시점은 Loon이 결정합니다. USB로 복사한 파일은 직접 교체하세요. 이전 버전으로 돌아가려면 구독 주소의 `main`을 원하는 커밋의 전체 해시로 바꿔 가져온 다음 기존 항목을 끄세요. [커밋 기록](https://github.com/lingjieheti/loon-adlite/commits/main/)

[앱별 적용 범위와 제한(중국어)](COVERAGE.md) · [후원하기(영어)](SPONSOR.en.md)
