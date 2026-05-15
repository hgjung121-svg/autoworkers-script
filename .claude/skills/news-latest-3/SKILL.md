---
name: news-latest-3
description: |
  매일 한국+글로벌 최신 경제 뉴스 3가지를 웹 검색으로 자동 수집·크로스체크하고,
  중학생도 이해할 수 있는 쉬운 언어로 심층분석 + 미래예측까지 담은
  시청자 대상 유튜브 롱폼 대본(10~15분) + 쇼츠 대본(60초×3개)을 자동 생성한다.

  팩트 크로스체크·감정 스토리텔링·구독자 감사 어조·SEO 최적화 제목/썸네일/이미지 프롬프트
  포함 풀패키지 출력. 13게이트 정책 안전 SSOT + AI 디스클레이머 5줄 + 한줄 대본 자동 생성
  + PD 직접 검증 강제 등 워크스페이스 운영 자산 전체 적용. 속보 모드 지원으로 이슈 발생
  즉시 단일 뉴스 속보 대본도 자동 생성 가능.

  다음 상황에서 반드시 이 스킬을 사용하라:
  - "최신뉴스 3" / "최신 뉴스 3개 대본" / "오늘 핵심 뉴스 3개"
  - "오늘 경제 뉴스 대본 써줘" / "경제 유튜브 대본 만들어줘"
  - "오늘 핵심 뉴스 뭐야 + 유튜브 만들게"
  - "쇼츠도 같이 만들어줘"
  - "속보 대본 써줘" / "방금 나온 뉴스로 영상 만들자" / "긴급 뉴스 영상"
  - "○○ 발표 났는데 대본 좀" (특정 이슈 즉시 대응)

  ⚠️ 레퍼런스 영상 분석이 필요한 ETF/교육/심층 시리즈는 이 스킬 대신 script-pd 사용.
---

# news-latest-3 스킬 — 최신 뉴스 3개 기반 유튜브 풀패키지 자동 생성

## 핵심 철학

> "구독자 한 분 한 분이 이 영상을 통해 오늘 하루 더 현명한 결정을 내릴 수 있도록."

- 구독자 입장에서 먼저 생각: "이 뉴스가 내 삶에 어떤 의미인가?"
- 시청자 시간에 항상 감사한 마음
- **팩트는 반드시 2개 이상 출처로 크로스체크** ([feedback_factcheck_required])
- **시행/현행 정책 단정 회피** — WebSearch 재검증 필수 ([feedback_factcheck_policy_implementation])
- 감정 곡선을 설계해 끝까지 보게 만든다
- **속도가 곧 조회수** — 이슈 발생 시 즉시 대응
- **13게이트 정책 안전 SSOT 자동 강제** ([feedback_youtube_13_gates])
- **AI 디스클레이머 5줄 의무** — YMYL 면책 + 채널 보호

---

## 모드 자동 선택

요청 분석 후 두 모드 중 하나:

### 📰 표준 모드 — 일일 브리핑 (기본값)
- 트리거: "최신뉴스 3", "오늘 경제 뉴스", "오늘 대본 써줘", 평일 정기 콘텐츠 요청
- 결과: 뉴스 3개 + 롱폼(10~15분) + 쇼츠 3개 + 풀패키지
- 파이프라인: STEP 1~9 전체 실행

### ⚡ 속보 모드 — Breaking News Mode
- 트리거 키워드 (메모리 [breaking-news-mode-track]):
  - "속보", "긴급", "방금", "지금 막", "터졌어"
  - "○○ 발표 났어", "○○가 발표했어"
  - "속보 대본", "긴급 뉴스 영상"
- 결과: 단일 뉴스 집중 롱폼(5~8분) + 쇼츠 1개 + SEO 패키지
- 파이프라인: STEP 1~9 중 속보용 트랙
- 처리 시간 목표: **총 15분 이내**
- 상세 절차: [`prompts/pd-script.md`](../../../prompts/pd-script.md) § BREAKING_NEWS_TRACK 참조

---

## 사전 확인 — 채널·프로젝트 셋업

### 채널 자동 선택
- 경제 뉴스 → `cclue-economy` 자동 ([feedback_economy_channel] 룰)
- 역사 뉴스 → `cclue-history` 자동 (예: 1592 임진왜란 사료 발견 속보)
- 기타: 사용자 확인

### 프로젝트 명명
- 표준: `news-{MMDD}-{slot}` (slot: morning/evening — settings에 따라)
- 속보: `breaking-{이슈키워드}-{MMDD}` (예: `breaking-bok-rate-cut-0515`)

### 디렉토리 구조 생성
```bash
python -c "import os; [os.makedirs(p, exist_ok=True) for p in [
  'channels/{채널}/projects/{프로젝트}/_refs',
  'channels/{채널}/projects/{프로젝트}/_script/shorts',
  'channels/{채널}/projects/{프로젝트}/output/thumbnails'
]]"
```

### Lazy Load 필수 자료
- `channels/{채널}/config/profile.md` — 채널 톤·정체성
- `channels/{채널}/config/settings.json` — shorts.enabled, 시그니처 등
- `channels/{채널}/config/pd-guide.md` (있으면) — 채널별 가이드
- `prompts/youtube-policy-gates.md` — 13게이트 SSOT (의무)
- `prompts/thumbnail-design.md` — 색상 심리학 4매트릭스 + 시니어 시인성
- `prompts/seo-titles.md` — 제목 A/B/C 패턴 SSOT
- `prompts/tts-rules.md` — TTS 검수 룰
- `prompts/quality-gates.md` — PD 직접 검증 SSOT

---

## 실행 파이프라인 (9단계)

### STEP 1. 오늘의 경제 뉴스 수집

#### 표준 모드 — WebSearch 6~8회
```
- "{TODAY} 한국 증시 마감 코스피"
- "{TODAY} 원달러 환율 유가"
- "{TODAY} 한국 경제 단독 속보"
- "{TODAY} 정부 발표 정책 새"
- "{TODAY} 기업 실적 발표 어닝쇼크"
- "today global economy news top stories"
- "{TODAY} 한국은행 기획재정부 발표"
- "{TODAY} 시니어 관련 경제 정책" (시니어 대상 채널이면)
```

#### 속보 모드 — 이슈 키워드 중심
```
- "{이슈} 속보 {TODAY}"
- "{이슈} 공식 발표"
- "{이슈} breaking news {TODAY}"
- "{이슈} 영향 분석"
- "{이슈} 비슷한 과거 사례"
```

#### 선정 기준
- 한국 2개 + 글로벌 1개 권장 (또는 큰 흐름으로 연결 가능한 조합)
- 시청자 삶에 직접 영향 우선 (물가·금리·부동산·연금·환율·주식·고용·의료비)
- 카테고리 중복 회피 ([feedback_topic_rotation_rule] — 같은 거대 주제 연속 2편까지)
- 표준: 후보 5~6개 → 3개 압축 / 속보: 단일 이슈 다각도

산출: `_refs/_news_candidates.md` (후보 + 선정 근거)

### STEP 2. 팩트 크로스체크 + 핵심 뉴스 선정

**필수 — 두 모드 공통.** 각 뉴스에 대해 **최소 2개 이상 출처** 추가 검색.

#### 신뢰 출처 우선순위
1. 정부·공공기관 (기재부, 한국은행, 통계청, 금감원, 국토부)
2. 글로벌 1차 (Fed, ECB, BOJ, IMF, OECD, 미 노동부)
3. 공신력 통신사 (연합뉴스, Reuters, Bloomberg, AP, WSJ)
4. 주요 경제지 (한국경제, 매일경제, FT, NYT)

#### 분류 (인라인 표기 의무)
- `[팩트]` — 2개 이상 출처 일치 (수치·날짜·발표 주체)
- `[분석]` — 전문가 해석·전망 → "~라는 분석"
- `[예측]` — 미래 전망 → "~될 가능성"
- `[미확인]` — 1개 출처만 → 제외 또는 "확인 중" 명시

**⚠️ 시행/현행 단정 회피 룰** ([feedback_factcheck_policy_implementation]):
- 정책·세제·법규의 "현행 시행 중" 단정은 WebSearch 재검증 필수
- 2023 ISA 확대 개편안을 시행으로 오인해 5편 라이브 영상 잘못된 정보 노출 사례
- 시행 미정 정책은 "확대 개편안 발표(시행 미정)" 식으로 명시
- ISA·세제 현재 수치는 [reference_korean_isa_tax_2026] 우선 참조

산출: `_script/factcheck.md` + `_script/verified-data.md`

### STEP 3. 감정 곡선 & 스토리 구조 설계

대본 작성 전 감정 곡선 먼저 설계:

> 충격/긴장(오프닝) → 공감/걱정(팩트) → 이해/안도(해설) → 궁금증(다음 뉴스) → 놀라움(분석) → 용기/행동(예측+제안) → 감사/따뜻함(아웃트로)

각 뉴스는 **문제 → 공감 → 해설 → 해결책** 구조.

#### 훅 유형 7종 (뉴스 성격 + 시청자 페인포인트 기반 선택)

상세 정의 → [`prompts/hook-types.md`](../../../prompts/hook-types.md)

1. **질문형**: "여러분, 내년에 대출 이자 얼마나 오를지 아세요?"
2. **충격형**: "오늘 아침, 한국인 3명 중 1명에게 영향 주는 뉴스가 나왔습니다"
3. **스토리형**: "서울 은평구 김 씨는 어제 아침 뉴스를 보고 깜짝 놀랐습니다"
4. **예언형**: "6개월 후, 우리 집 전기세가 지금보다 30% 오를 수 있습니다"
5. **대비형**: "준비한 사람과 준비 못 한 사람, 1년 후 차이가 납니다"
6. **속보형** (속보 모드): "지금 막 들어온 소식입니다. 오늘 오후 [시각], [기관]에서 [발표]"
7. **긴급 행동형** (속보 모드): "이 영상을 보시는 지금 당장 확인하셔야 할 게 있습니다"

산출: `_script/concept.md` (감정 아크 + 훅 유형 + 스토리 구조 명시)

### STEP 4. 대본 작성 — 언어 & 어조 규칙

#### 언어 원칙
- 중학생이 들어도 이해되는 언어 ([feedback_retention_general_viewer])
- 경제 용어는 **반드시 괄호로 설명** — 예: 금리(은행에서 돈 빌릴 때 내는 이자 비율)
- 비유와 예시 적극 — "금리 인상은 마치 은행이 대출 문을 조금씩 닫는 것"
- 짧은 문장 (한 문장에 한 가지 정보)
- 숫자는 구체적·비교로 체감 — "1달러 1,400원 → 해외여행 경비가 작년보다 10만원 더 드는 셈"
- 팩트/분석/예측 구분 표기

#### 어조 원칙
- 따뜻하고 신뢰감 있는 선배·전문가 말투
- 뉴스 앵커 말투 금지
- 시청자 호칭: "여러분"
- 감사 표현 자연스럽게:
  - "바쁘신 중에 이 영상 찾아주셔서 정말 감사합니다"
  - "끝까지 봐주셔서 고맙습니다. 오늘도 현명한 하루 되세요"

#### 🔴 13게이트 SSOT 사전 회피 (8개 작성 단계 우선 룰)
[`prompts/youtube-policy-gates.md`](../../../prompts/youtube-policy-gates.md) — 의무 적용

1. **단정 표현 금지** — "확정/100%/무조건/사라/팔아라" → "가능성/전망/주목할" 치환
2. **종목 비중 권고 reject** — "X 70/Y 30" 금지 → "본인 위험 성향에 따라"
3. **모든 통계·수치에 출처 인라인** — "한국은행에 따르면", "통계청 자료" 등
4. **정치·민감 주제 가드** — 1차 출처 2개 + "추정/주장" 표현 강제
5. **숫자 카운트** — 전체 30개 이하 + 파트당 2개 이하 ([feedback_deep_analysis_over_numbers])
6. **🔴 5개 고위험 게이트** (3·5·11·12·13) 작성 단계 우선 회피
7. **AI 도입·결론 패턴 회피** — "오늘은 ~에 대해 알아보겠습니다" 금지
8. **메타데이터 약속 이행** — 제목·썸네일 약속은 본문 20% 이내 등장

### STEP 5. 롱폼 대본 구조

#### 표준 모드 (10~15분 = 4,000~6,000자)

```
1. 오프닝 훅 (30~45초, 200~300자)
2. 구독·좋아요·알림 요청 (20~30초, 130~200자)
   ⚠️ CTA 위치: 훅+인트로 직후 초반 ([feedback_cta_position])
   ⚠️ 직접 나열 금지, 자연스럽게 유도 ([feedback_cta_rule])
3. 오늘 다룰 내용 예고 (30초, 200자)
4. 뉴스 1 (4~5분, 1,600~2,000자):
   팩트(1분) → 공감 브리지(30초) → 쉬운 해설(1~2분) → 심층 분석(1분) → 예측 3시나리오+행동 제안(1분)
5. 뉴스 2 (4~5분) — 동일 구조, 훅 변주
6. 뉴스 3 (4~5분) — 동일 구조
7. 오늘 핵심 정리 + 인사이트 (1~2분, 400~800자)
8. 아웃트로 클로징 (30~40초, 200~270자)
   ⚠️ Q3 약속형 회피 ([feedback_q3_promise_avoidance]) — "근접한 3명 다음 영상" 금지
   대신 통제감 클로징: "여러분 댓글 하나하나 다 봅니다" / "다음 영상도 준비 중"
```

#### 속보 모드 (5~8분 = 2,000~3,200자)
[`prompts/pd-script.md`](../../../prompts/pd-script.md) § BREAKING_NEWS_TRACK 단계 2 참조

### STEP 6. 쇼츠 대본 자동 생성

상세 절차 → [`prompts/pd-script.md`](../../../prompts/pd-script.md) § SHORTS

**채널 `settings.json`의 `shorts.enabled`가 true 또는 사용자 명시 요청 시만 실행.**

- 표준 모드: 60초×3 (충격 수치형 / 반전·진실형 / 행동 가이드형)
- 속보 모드: 60초×1 (가장 자극적인 단면)
- 산출: `_script/shorts/shorts_01~03.txt` + `shorts_meta.json` + `shorts_oneline.txt`

### STEP 7. SEO 최적화 제목 작성

**SSOT** → [`prompts/seo-titles.md`](../../../prompts/seo-titles.md) — A/B/C 3패턴 공식

#### 3패턴 (각각 1개씩 총 3안 제시 — [feedback_title_options])
- **패턴 A** — 숫자+위기+행동형 (CTR 최강)
- **패턴 B** — 질문+공감형 (체류시간 ↑)
- **패턴 C** — 속보+권위형 (속보 모드 전용)

각 후보 옆에 `[예상 강점]` 메모. 사용자가 A/B 테스트 선택.

#### 필수 룰
- 앞 30자 안에 핵심 키워드 배치 (모바일 잘림 대응)
- 전체 50~60자
- 숫자 1개 이상
- 감정 단어 (충격·비상·긴급·꼭·반드시) — 단, 거짓 클릭베이트 금지
- 대괄호 활용: `[속보]`, `[발표]`, `[심층분석]`
- 부등호 사용 금지 ([feedback_youtube_no_angle_brackets]) — `<1` → "1 미만"

### STEP 8. SEO 최적화 썸네일 설계

상세 → [`prompts/thumbnail-design.md`](../../../prompts/thumbnail-design.md)

#### 시니어 시인성 3원칙 (cclue-economy 의무)
1. 큰 글씨, 높은 대비
2. 감정이 보이는 인물
3. 숫자·기호 강조

#### 색상 심리학 4매트릭스 ([feedback_thumbnail_color_psychology])
prompts.json `meta.color_psychology`에 1개 선택 + HEX 명시:
- 위기 알림: `#E63946`+`#FFD60A`+`#1D1D1D`
- 기회 포착: `#FFFFFF`+`#06A77D`+`#003566`
- 행동 가이드: `#1D1D1D`+`#FFD60A`+`#FFFFFF`
- 비교 대비: `#E63946`↔`#06A77D`+`#1D1D1D`

#### 추가 룰
- ⚠️ 환각 방지 부정형 표현 금지 ([feedback_thumbnail_no_hallucination_guard])
- ⚠️ Gemini 거부 회피 ([feedback_gemini_image_avoidance]) — 한국·정치·실존 인물 표현 대체
- ⚠️ 다중 플랫폼 호환 ([feedback_thumbnail_multi_platform]) — `platforms` 필드 + 한글 렌더링 명확화

산출: `output/thumbnails/prompts.json`

### STEP 9. 업로드 패키지 풀세트 출력

#### 9-1. 제목 후보 3개 (A/B/C 각 1개) + 예상 강점

#### 9-2. youtube.md 설명란
- **상단 5개 해시태그** ([feedback_description_hashtags])
- **본문 첫 100자 SEO 키워드 5~7개 자연 분산** ([feedback_description_first_100_chars])
- **AI 디스클레이머 5줄** ([feedback_youtube_policy_safety]) 본문 끝 의무 삽입
- **챕터 타임스탬프 10개 이상**
- **하단 20개 해시태그**
- 부등호 사용 금지

포맷 → [`prompts/pd-templates.md`](../../../prompts/pd-templates.md) § youtube.md

#### 9-3. 한줄 대본 ([feedback_script_oneline])
- `_script/script-oneline.txt` 의무 생성

#### 9-4. 쇼츠 세트 (shorts.enabled=true 시)

#### 9-5. 태그·키워드·카테고리 — pd-templates.md 포맷 따라

#### 9-6. (옵션) Downloads 자동 복사 ([feedback_thumbnail_download_copy])
- 사용자 명시 요청 시만 실행 ([feedback_thumbnail_prompt_only])

---

## PD 직접 검증 (완료 선언 전 의무)

[`prompts/quality-gates.md`](../../../prompts/quality-gates.md) — 5게이트 SSOT

### 핵심 룰 ([feedback_verify_before_complete])
1. 에이전트 자가 보고는 검증의 시작, 끝이 아니다 — PD 무조건 Grep 직접 재검증
2. 검색 패턴 변형 18개 이상 — 좁은 패턴은 누락 보장
3. 0건 확인 전 "완료" 선언 금지 — 잔존 발견 시 PD 직접 정리
4. 같은 누락 2회 이상 = 에이전트 신뢰 정지, PD 직접 마무리

### 자동화 레이어
- **PostToolUse Hook**: `.claude/hooks/verify-consistency.py` — 산출물 변경 시 자동 알림
- **슬래시 커맨드**: `/verify {프로젝트}` — 전수 검증

---

## 완료 보고 ([feedback_proactive_report])

작업 완료 즉시:
- 프로젝트명, 채널명
- 산출물 경로 + 글자수 + 예상 분량
- 다음 행동 (썸네일 이미지 생성? 시청자 응대? 등)
- 사용자가 묻기 전 선제 보고

```
=== news-latest-3 패키지 완성 ===

프로젝트: channels/cclue-economy/projects/news-{MMDD}-evening/
채널: 깊이 읽는 경제 (cclue-economy)
모드: 표준 / 속보

산출물:
  ✅ _script/script.txt (4,823자, ~12분)
  ✅ _script/script-oneline.txt (한줄 버전)
  ✅ _script/shorts/shorts_01~03.txt (쇼츠 ON이면)
  ✅ _script/shorts/shorts_meta.json
  ✅ output/youtube.md (제목 3안 + 디스클레이머 5줄 + 100자 키워드)
  ✅ output/thumbnails/prompts.json (color_psychology=위기 알림)

13게이트 검증: 🔴 0건 / 🟡 0건 / 🟠 0건
PD Grep 변형 18+ 통과

다음 행동:
  → 썸네일 이미지 생성 원하시면 "썸네일 만들어줘" 입력
  → 또는 그대로 영상 제작 사이트 업로드 가능
```

---

## 트리거 키워드 (CLAUDE.md 등록)

다음 발화에서 이 스킬을 자동 호출:
- "최신뉴스 3", "최신 뉴스 3개"
- "오늘 경제 뉴스 대본"
- "오늘 핵심 뉴스 + 유튜브"
- "속보 대본", "긴급 뉴스 영상", "방금 나온 뉴스로 영상"
- "○○ 발표 났는데 대본"

레퍼런스 영상 분석이 필요한 경우(ETF 시리즈/심층 시리즈)는 이 스킬 대신 [script-pd](../script-pd/SKILL.md) 호출.
