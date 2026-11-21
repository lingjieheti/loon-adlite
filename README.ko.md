# 아이폰·아이패드용 경량 Loon 광고 필터

[简体中文](README.md) · [繁體中文](README.zh-Hant.md) · [English](README.en.md) · [日本語](README.ja.md) · **한국어** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [Русский](README.ru.md) · [Français](README.fr.md) · [Español](README.es.md) · [العربية](README.ar.md)

제가 아이폰과 아이패드에서 함께 쓰는 구독을 중국에서 생활하는 유학생 등 중국 앱을 자주 쓰는 분들과 공유합니다. 징둥·타오바오·메이퇀 같은 중국 앱이나 웹에서 요청을 보낼 때 호스트 이름이 목록의 광고 도메인과 정확히 일치하면 기기에서 차단합니다. 앱 안에 표시되는 일부 광고까지 걸러내려면 지정된 요청에만 적용되는 로컬 재작성 규칙을 켤 수 있습니다.

## 설치

**[통합판 설치](https://www.nsloon.com/openloon/import?plugin=https%3A%2F%2Fraw.githubusercontent.com%2Flingjieheti%2Floon-adlite%2Fmain%2FiPad-AdSuite.lpx)** · [구독 주소](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/iPad-AdSuite.lpx)

아이폰이나 아이패드의 Safari에서 설치 링크를 열고 Loon에서 가져오기를 승인하세요. Loon의 설정 → 플러그인 → ＋에 구독 주소를 붙여 넣어도 됩니다. 도메인 차단에는 인증서가 필요 없습니다. 플러그인은 기기 안에서 작동하며 원격 스크립트를 불러오거나 사용 기록을 수집하지 않습니다.

기존 통합판(Suite) 구독자는 구독을 새로 고치면 됩니다. 이 프로젝트의 다른 광고 차단 플러그인을 사용했다면 통합판을 켠 뒤 기존 항목을 꺼서 규칙이 중복되지 않도록 하세요.

## 앱 화면에 포함된 광고

위챗 공식 계정의 글이나 빌리빌리 홈 피드에서 일부 광고를 걸러내려면 Loon 3.5.1(빌드 978) 이상에서 재작성과 지정 호스트의 HTTPS 복호화를 켜고 기기에서 직접 생성한 Loon 인증서를 신뢰하세요. 같은 호스트의 다른 요청도 복호화될 수 있고 연결 및 응답 처리에 시간이 더 걸립니다. [Loon의 HTTPS 복호화 안내](https://nsloon.app/docs/MitM/)

더우인 추천 피드 규칙은 샘플 응답으로 테스트했습니다. 현재 앱에서의 실제 효과는 아직 확인이 필요합니다. 영상에 녹화된 협찬 구간은 직접 건너뛰어야 합니다.

## Safari 선택 기능

YouTube 웹 도우미는 공식 광고 건너뛰기 버튼이 나타나면 클릭을 시도합니다. 별도 도우미로 Pornhub의 일부 광고 영역을 숨길 수도 있습니다. [YouTube 스크립트](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/youtube/youtube.user.js) · [Pornhub 스크립트](https://raw.githubusercontent.com/lingjieheti/loon-adlite/main/web/pornhub.user.js)

## 업데이트

GitHub는 매일 광고 호스트 목록을 원본과 대조하고 매번 보안 감사를 수행합니다. 승인된 호스트 목록이 바뀌면 감사와 모든 테스트를 통과한 뒤에만 기존 구독 주소로 자동 배포합니다. 빌리빌리와 징둥 등 앱 내 광고 필터의 원본도 매일 확인하며, 필터를 수정할 때는 배포 전에 별도 보안 검토를 거칩니다.

구독 주소는 `main`을 따릅니다. Loon의 외부 리소스 업데이트 확인 주기를 하루로 설정할 수 있습니다. 이전 버전으로 돌아가려면 구독 주소의 `main`을 원하는 커밋의 전체 해시로 바꾸세요. [커밋 기록](https://github.com/lingjieheti/loon-adlite/commits/main/)

[앱별 적용 범위와 제한(중국어)](COVERAGE.md) · [기능별 출처(중국어)](SOURCES.md) · [오프라인 회귀 테스트](tests/) · [후원하기(영어)](SPONSOR.en.md) · [보안 감사(중국어)](SECURITY-AUDIT.md)
