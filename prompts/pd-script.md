# 대본 제작 — 상세 절차

`{P}` = `channels/{채널}/projects/{프로젝트}`
`{VENV_PYTHON}` = macOS/Linux: `.venv/bin/python` | Windows: `.venv\Scripts\python`

---

## COLLECT

**YouTube 레퍼런스 수집.**

1. 사용자에게 YouTube URL 수집 (또는 이미 있으면 확인)
2. 실행:
```bash
{VENV_PYTHON} scripts/collect.py --project {프로젝트} --channel "{채널}" URL1 URL2 ...
```
3. 결과: `_refs/{NNN}/` 에 meta.md, transcript.txt, thumbnail.webp

### collect.py 실패 시 — 수동 수집 폴백

collect.py가 실패하면 (429 에러, 네트워크 문제 등) 사용자에게 대본을 직접 붙여넣도록 안내한다.

**흐름 — 한 번에 하나씩, 제목과 대본을 분리해서 받는다:**

```
1. 안내: "YouTube에서 직접 가져오지 못했습니다. 대본을 직접 붙여넣어 주세요."
2. 요청: "첫 번째 레퍼런스 영상의 제목을 알려주세요."
3. 사용자가 제목 입력
4. 요청: "이제 그 영상의 대본을 붙여넣어 주세요."
5. 사용자가 대본 붙여넣기
6. _refs/001/ 생성 (transcript.txt + meta.md)
7. 질문: "두 번째 레퍼런스 영상도 있나요?"
8. 있으면 → "제목을 알려주세요." → "대본을 붙여넣어 주세요." → _refs/002/ 생성
9. 반복 (최대 4~5개)
10. 없으면 → ANALYZE 진행
```

**파일 생성 규칙:**
- `_refs/{NNN}/transcript.txt` — 사용자가 붙여넣은 대본 텍스트 그대로 저장
- `_refs/{NNN}/meta.md` — 최소 정보로 생성:
  ```markdown
  # {영상 제목}

  ## 기본 정보
  - **URL**: {있으면 URL, 없으면 "(직접 입력)"}
  - **수집 방식**: 수동 입력
  ```
- `thumbnail.webp` — 없음 (수동 수집이므로 썸네일 없이 진행)

---

## ANALYZE

**레퍼런스 영상 분석. 에이전트: video-analyst**

1. `_refs/*/analysis.md`가 없는 영상 목록 확인
2. **전체 동시 병렬 실행** (run_in_background: true, **TaskOutput 사용 금지** → Glob으로 확인)
3. 각 에이전트에게 전달:
   - 채널 프로필 (`channels/{채널}/config/profile.md`)
   - 분석 프롬프트 (`prompts/reference-analyze.md`)
   - 영상 데이터 (meta.md + transcript.txt + thumbnail.webp)
4. 출력: 각 `_refs/{NNN}/analysis.md`
5. 완료 후 요약 보고

---

## DATA_PREP

**패턴 추출 + 데이터 검증/리서치. 2 에이전트 완전 병렬.**

### pattern-extractor 에이전트

1. 최소 2개 analysis.md 필요 (부족하면 알림)
2. 에이전트 1개 호출 (run_in_background: true)
3. 전달: 채널 프로필 + `prompts/reference-patterns.md` + 모든 analysis.md + meta.md
4. 출력: `{P}/_script/patterns.md`

### data-researcher 에이전트

1. 에이전트 1개 호출 (run_in_background: true, WebSearch 사용)
2. 전달: 채널 프로필 + `prompts/data-research.md` + 모든 transcript.txt + 모든 analysis.md
3. 출력: `{P}/_script/factcheck.md` + `{P}/_script/verified-data.md` (추가 리서치 포함)

### 완료 확인

- `_script/patterns.md` 존재 확인
- `_script/verified-data.md`에 "## 추가 리서치" 존재 확인

---

## STRATEGY

**크리에이티브 전략 통합 설계 + 썸네일 프롬프트. strategist 에이전트 1회.**

입력: `_script/patterns.md` + `_script/verified-data.md` + 채널 프로필

### 사전 준비

```bash
python -c "import os; os.makedirs('{P}/output/thumbnails', exist_ok=True)"
```

### strategist 에이전트 호출

1. strategist 에이전트 호출:
   - 전달: `prompts/creative-strategy.md` 내용 + `prompts/ctr-reference.md` 내용
          + `prompts/thumbnail-design.md` 내용
          + 채널 프로필 + `config/pd-guide.md` (있으면)
          + `config/thumbnail-strategy.json` (있으면)
          + `config/assets/mascot/` 경로 (있으면)
          + `_script/patterns.md` 경로 + `_script/verified-data.md` 경로
          + `{P}/_refs/` 경로
          + 모드 (auto / ask)
   - auto 출력: `{P}/_script/concept.md` + `{P}/_script/hook-intro.md` + `{P}/output/thumbnails/prompts.json`
   - ask 출력: `{P}/_script/_strategy_candidates.md`

### auto 모드

1. concept.md + hook-intro.md + prompts.json 존재 확인
2. 결과 요약 보고
3. 백그라운드 썸네일 이미지 생성 (fire-and-forget, prompts.json 존재 시):
```bash
{VENV_PYTHON} scripts/src/thumbnail/generate_thumbnails.py \
  --project {프로젝트} --channel "{채널}"
```
   - `run_in_background: true`로 실행, 완료 대기 없이 즉시 다음 단계 진행
4. OUTLINE 진행

### ask 모드

1. `_strategy_candidates.md` 읽기
2. 3 패키지 사용자에게 제시 (컨셉+제목+Hook 간결 비교)
3. 사용자 선택/수정/혼합:
   - "B로 해줘" → B 그대로 채택
   - "A 앵글에 B 제목으로" → 혼합
   - "A 좋은데 Hook 좀 바꿔줘" → 수정
4. 확정 → `_script/concept.md` + `_script/hook-intro.md` 저장
5. 썸네일 프롬프트 생성: `{S}/concept.md`의 썸네일 이미지 컨셉 + `prompts/thumbnail-design.md` 규칙 + `_refs/` 썸네일 분석으로 `{P}/output/thumbnails/prompts.json` 생성 (PD 직접 또는 strategist Phase 5 호출)
6. 백그라운드 썸네일 이미지 생성 (fire-and-forget, prompts.json 존재 시):
```bash
{VENV_PYTHON} scripts/src/thumbnail/generate_thumbnails.py \
  --project {프로젝트} --channel "{채널}"
```
   - `run_in_background: true`로 실행, 완료 대기 없이 즉시 다음 단계 진행
7. OUTLINE 진행

---

## OUTLINE

**통합 기획서 작성. PD 직접 수행.**

입력: `_script/concept.md` + `_script/hook-intro.md` + `_script/patterns.md` + `_script/verified-data.md` + 채널 프로필

### ask 모드
1. 통합 기획서 초안 제시 (포맷은 `prompts/pd-templates.md` 참조)
2. 사용자 검토/피드백 → 수정 → 확정
3. `_script/outline.md` 저장

### auto 모드
1. 오케스트레이터가 outline.md 직접 생성 (셀프체크 9항목 내장):
   1. 제목→구조 정합성
   2. 감정 전략 정합성
   3. 완시율 설계
   4. 핵심약속 이행
   5. 스테이크 상승
   6. 재참여 포인트 (2~3분 간격)
   7. 데이터 활용 검증 (verified-data.md에 존재하는 데이터만)
   8. 분량 현실성 (1분≈400자)
   9. 대본 작성 가능성
2. `_script/outline.md` 저장 → 바로 DRAFT 진행

### 제목→구조 제약 규칙

확정 제목이 본문 구조를 제약한다. 반드시 확인:

| 제목 패턴 | 구조 제약 |
|-----------|----------|
| "N가지 이유/방법/실수" | 정확히 N개 섹션 |
| "~의 몰락/추락/붕괴" | 시간순 서사 |
| "A vs B" 비교 | 비교 프레임워크 |
| "진짜 이유/숨겨진 비밀" | 미스터리 구조 (표면→단서→진실) |
| "~하는 법" | 프로세스 구조 |

concept.md의 서사 유형과 확정 제목이 호환되는지도 확인한다. 비호환 시 서사 유형을 제목에 맞춰 조정.

### 타겟 러닝타임 결정 가이드

프로젝트 초기화 시 사용자에게 받은 `target_minutes`를 기준으로 한다:
1. **target_minutes** 확인 (사용자가 프로젝트 시작 시 지정한 목표 분량)
2. 확정 제목이 암시하는 섹션 수 반영 (예: "3가지 이유" → 3섹션 × 각 2~3분 + Hook/클로징)
3. 콘텐츠 볼륨 고려 (verified-data.md 데이터량, 사례 수)
4. 위 요소를 종합하여 target_minutes ±20% 범위 내에서 최종 러닝타임 결정
5. 최종 러닝타임을 outline.md `## 1. 기획 뼈대`의 `타겟 러닝타임`에 기록

### 본문 구조 가이드
- 모든 파트가 핵심약속 이행에 기여
- 핵심 포인트 3~5개를 가치 상승 순서로 배열
- 파트 전환 직전에 오픈루프 배치
- 1~2분 간격으로 소규모 리텐션 장치(질문, 반전, 감정 전환) 배치
- patterns.md의 검증된 리텐션 장치(오픈루프, 전환문구, 감정유발)를 리텐션 설계 섹션에 발췌 기록
- 각 파트에 예상 시간/글자수 (1분 ≈ 400자)

### 리텐션 설계 가이드
- **재참여 포인트**: 파트 전환점마다 + 긴 파트 중간에 배치하여 2~3분 간격 유지. 타겟 러닝타임 전체에 걸쳐 빈 구간 없이 분포
- **스테이크 상승**: 파트가 진행될수록 "왜 이게 중요한가"의 규모가 커져야 함
- **감정 목표**: 각 파트별 시청자의 감정 상태를 명시 (예: 충격→분석→공감→경각심)

**저장 후: 사용자 확인 없이 바로 DRAFT 단계로 자동 진행한다.**

---

## DRAFT

**대본 초안 작성. 에이전트: script-writer (파트당 1개, 병렬)**

입력: `_script/outline.md` + `_script/concept.md` + `_script/verified-data.md` + 채널 프로필 + `prompts/script-review-checklist.md`

### 🔴 안전 게이트 (script-writer 호출 시 명시 전달 필수)

**SSOT**: [`prompts/youtube-policy-gates.md`](youtube-policy-gates.md) — 13개 정책 안전 게이트 전체 정의 (위반 시 채널 삭제·수익화 정지·법적 리스크). script-writer는 이 SSOT를 받아 작성 단계에서 13게이트를 사전 회피해야 한다.

**작성 단계 우선 적용 룰** (DRAFT에서 reviewer 진입 전 차단):

1. **단정 표현 금지** (게이트 4 — YMYL) — "확정/100%/무조건/뚫는다/사라/팔아라/절대" → "가능성/전망/돌파 시나리오/주목할/통상" 치환
2. **종목 비중 권고 reject** (게이트 4 — 금감원 유사투자자문업 회피) — "X 70/Y 30" 같은 구체 비중 금지. 조건부 표현("본인 위험 성향에 따라")으로 변환
3. **모든 통계·수치에 출처 인라인 표기** (게이트 4·9) — "한국은행에 따르면", "맥쿼리 리포트", "통계청 자료" 등. 출처 없는 숫자 = reject
4. **정치·민감 주제 가드** (게이트 5 — 혐오 발언·🔴) — 계엄/부정선거/음모론은 1차 출처 2개 이상 + "추정/주장" 표현 강제. 보호 그룹 비하·비인간화·폭력 선동 금지.
5. **숫자 카운트 한도** (리텐션) — 전체 30개 이하 + 파트당 2개 이하. DRAFT 작성 후 즉시 검증:
   ```bash
   .venv/Scripts/python scripts/src/check_numbers.py {P}/_script/script.txt
   ```
   exit 1이면 부분 재작성. (2026-04-24 100개 사고 재발 방지)
6. **🔴 5개 고위험 게이트 사전 회피** (3·5·11·12·13) — 허위 조작·혐오 발언·아동 안전·자살 자해·극단주의. 1건 위반으로 채널 즉시 삭제. SSOT의 🔴 섹션 작성 단계에서 우선 회피.
7. **AI 도입·결론 패턴 회피** (게이트 1) — "오늘은 ~에 대해 알아보겠습니다", "결론적으로 ~입니다" 같은 AI 전형 패턴 금지. 자연스러운 구어체로 작성.
8. **메타데이터 약속 이행** (게이트 2) — 제목·썸네일에서 약속한 핵심 내용은 본문 이내 20% 이내에 등장해야 함.

근거: SSOT [youtube-policy-gates.md](youtube-policy-gates.md) — 한국 12-24 허위정보 손배법(5배 징벌) + 금감원 유사투자자문업 신고 의무 + YouTube 13개 정책 안전 게이트 + 시청자 리텐션 (메모리 [feedback_deep_analysis_over_numbers]).

### 파트별 병렬 에이전트

1. outline.md `## 3. 본문 구조`에서 `### ` 파트 헤더 추출 → 파트 목록 확인
2. **Hook & Intro는 에이전트 범위에서 제외** — merge_draft.py가 자동 삽입
3. 파트당 에이전트 1개 병렬 호출:
   - 각 에이전트 → `_script/_draft_part{N}.md` 저장 (N = 파트 순서, 클로징 포함)
4. 각 에이전트에게 전달: outline.md(담당 파트 섹션) + concept.md + verified-data.md + 채널 프로필 + script-review-checklist.md + 담당 파트명 + 출력 경로
5. 완료 확인: `ls {S}/_draft_part*.md`로 파일 수 == 파트 수

### draft.md 병합

```bash
{VENV_PYTHON} scripts/src/merge_draft.py \
  --hook-intro {S}/hook-intro.md \
  --parts-dir {S} \
  --output {S}/draft.md
```

### 분량 검증 게이트 (REVIEW 전 필수)

```bash
{VENV_PYTHON} scripts/src/validate_draft.py {S}/outline.md {S}/draft.md --threshold 0.9
```

- **exit 0** (전 파트 90% 이상) → REVIEW 진행
- **exit 1** (FAIL 파트 있음) → 보충 2-pass:
  1. FAIL 파트 번호(N) 확인
  2. outline.md에서 빠진 내용(비유/사례/데이터) 식별
  3. script-writer 재호출 → `_draft_part{N}.md` 덮어쓰기
  4. merge_draft.py 재실행 → draft.md 재생성
  5. validate_draft.py 재실행 (1회)

---

## REVIEW_FINALIZE

**검수 + 확정. 에이전트: script-reviewer(verdict 권한 + 신규 주장 WebSearch 검증)**

1. **script-reviewer 에이전트 호출:**
   - 전달: `_script/draft.md` + `_script/outline.md` + `_script/concept.md` + `_script/verified-data.md` + `prompts/script-review-checklist.md` + `prompts/draft-verify.md`
   - 출력: `{P}/_script/review.md` (체크리스트 + 심각도 분류 + 신규 주장 검증 결과 + verdict)
   - reviewer가 신규 주장을 식별하면 즉시 WebSearch로 검증하여 review.md에 포함

2. **verdict 확인:**
   - review.md의 `verdict:` 확인
   - `verdict: 통과` → finalize.py 실행
   - `verdict: 수정` → 리비전 1회

3. **리비전 (최대 1회):**
   - review.md 치명적 항목 (신규 주장 ❌/⚠️ 포함) 정리
   - script-writer 재호출 → draft.md 덮어쓰기
   - finalize.py 실행 (재검수 없이 확정)

4. 확정 후 finalize:
```bash
{VENV_PYTHON} scripts/finalize.py --project {프로젝트} --channel "{채널}"
```
5. 결과: `{P}/_script/script.txt` (순수 텍스트, 한 줄 형태)

6. **TTS 검수:**
   - `{P}/_script/script.txt` 읽기
   - `prompts/tts-rules.md` 규칙에 따라 형식만 정리 (내용 변경 금지)
   - 정리된 텍스트를 `{P}/_script/script.txt`에 덮어쓰기

---

## SHORTS

**롱폼에서 60초 쇼츠 3개 자동 추출. PD 직접 수행. 채널이 쇼츠 ON 일 때만 실행.**

### 전제 조건
- `{P}/_script/script.txt` 존재
- `channels/{채널}/config/settings.json`의 `shorts.enabled: true` (없으면 기본 false — 명시적으로 켜야 함)
- 또는 사용자가 "쇼츠도 만들어줘" 요청

### 사전 준비
```bash
python -c "import os; os.makedirs('{P}/_script/shorts', exist_ok=True)"
```

### 추출 절차

**입력**: `{P}/_script/script.txt` + `{P}/_script/verified-data.md` + `{P}/_script/concept.md` + 채널 프로필

**원칙**: 본문에서 **새 정보를 짓지 않는다**. 본문에 이미 검증된 사실·수치만 쇼츠로 압축. 본문에 없는 통계는 verified-data.md에서만 가져온다.

#### 쇼츠 3개 선정 기준 (우선순위)
1. **충격 수치형** — 숫자 1개로 클릭이 잡히는 컷 (가장 큰 숫자/가장 작은 숫자/비교)
2. **반전·진실형** — "사실 ~입니다", "실제로는 ~", 본문 핵심 인사이트 1줄로 압축
3. **행동 가이드형** — "지금 ~하세요", "오늘 ~확인하세요" 식 즉시 실행 가능 1가지

> 속보 모드인 경우 1개만 생성 (단일 이슈의 가장 자극적인 단면).

#### 쇼츠 1개당 60초 구조 (170~200자 / 한 문장 최대 15자)

```
[0~5초]   강한 훅 한 줄 (질문형 또는 충격형)
[5~15초]  핵심 팩트 1~2줄 (수치 포함, 출처 인라인)
[15~45초] 쉬운 해설 + 비유 (왜 중요한지)
[45~55초] 시청자 행동 제안 1줄
[55~60초] CTA ("구독하면 매일 이런 뉴스" — 본 채널 톤에 맞춰)
```

#### 안전 게이트 (롱폼과 동일하게 13게이트 SSOT 적용)
- 단정 표현 금지 / 종목 비중 금지 / 출처 인라인 / AI 도입 패턴 회피
- 쇼츠는 짧은 만큼 단정 위험이 높음 → "~로 보입니다", "~할 가능성" 표현 강제
- 모든 수치에 출처 ("한국은행에 따르면", "통계청 자료" 등) 1초라도 노출

### 산출물

1. **`{P}/_script/shorts/shorts_01.txt` ~ `shorts_03.txt`** — 각각 60초 분량 순수 텍스트 (한 줄 형태, TTS 입력용)
2. **`{P}/_script/shorts/shorts_meta.json`** — 쇼츠별 메타데이터:
   ```json
   {
     "shorts": [
       {
         "id": 1,
         "type": "충격 수치형",
         "title": "{40자 이내 쇼츠 제목 — 첫 화면 카피}",
         "hook_seconds_5": "{훅 첫 5초 문장}",
         "char_count": 187,
         "hashtags": ["#경제", "#금리", ...],
         "cover_prompt_en": "{Midjourney/DALL-E용 영문 커버 이미지 프롬프트, thumbnail-design.md 7요소 적용}"
       },
       ...
     ]
   }
   ```
3. **`{P}/_script/shorts/shorts_oneline.txt`** — 3개 쇼츠를 한 줄씩 모은 미리보기

### 검증
- 각 쇼츠 글자수 170~200자 (`len()` 확인)
- 한 문장 최대 15자 (긴 문장은 줄바꿈 또는 분할)
- 13게이트 SSOT 통과 (Grep 변형 패턴으로 단정·종목·AI 패턴 확인)
- 모든 수치 출처 인라인 1회 이상

---

## BREAKING_NEWS_TRACK (속보 모드)

**일반 파이프라인을 단축하여 15분 내에 5~8분 단일 이슈 영상 + 60초 쇼츠 1개를 산출.**

### 진입 조건
SKILL.md § 모드 결정의 속보 트리거 키워드 감지 → 이 트랙으로 분기.

### 프로젝트 명명
- 영문 kebab-case + `breaking-` 접두어 + 핵심 이슈 키워드
- 예: `breaking-bok-rate-cut-0515` / `breaking-housing-policy-1107`
- 채널은 메모리 `feedback_economy_channel.md`에 따라 cclue-economy 자동 (경제 이슈) / 역사·정치는 사용자 확인

### 1단계: 자료 수집 (5분 이내)

WebSearch 5~6회 + WebFetch 3~5개. **레퍼런스 영상 수집 건너뜀**.

```
WebSearch:
- "{이슈 키워드} 속보 {TODAY}"
- "{이슈 키워드} 공식 발표"
- "{이슈 키워드} breaking news {TODAY}"
- "{이슈 키워드} 영향 분석"
- "{이슈 키워드} 비슷한 과거 사례"

WebFetch (공식 1차 출처 우선):
- 정부·공공기관 발표문 원문
- 한국은행/기재부/금감원/Fed/ECB 등 보도자료
- 공신력 통신사(연합뉴스/Reuters/Bloomberg) 1보
```

산출: `{P}/_script/factcheck.md` + `{P}/_script/verified-data.md`

**크로스체크 분류 (인라인 표기 필수)**:
- `[팩트]` — 2개 이상 출처 일치 (수치·날짜·발표 주체)
- `[분석]` — 전문가 해석·전망
- `[예측]` — 미래 전망 ("~될 가능성")
- 1개 출처만이면 제외 또는 "현재까지 확인된 내용" 명시

### 2단계: 5~8분 단일 DRAFT (8분 이내)

레퍼런스 분석·STRATEGY·OUTLINE 생략하고 PD가 직접 작성 (단일 이슈 + 짧은 분량이라 에이전트 위임 오버헤드가 더 큼).

**구조 (5~8분 = 2,000~3,200자)**:

```
1. 속보 훅 (20~30초, 130~200자)
   - 훅 유형 6 (속보형) 또는 7 (긴급 행동형)
   - "지금 막 들어온 소식입니다. 오늘 오후 [시각], [기관]에서 [발표]"
   - 또는 "이 영상을 보시는 지금 당장 확인하셔야 할 게 있습니다"

2. 구독·알림 요청 (15초, 100자)
   - "이런 속보 빨리 받아보고 싶으시면 알림 설정해 두세요"

3. 무슨 일인가 (1~1.5분, 400~600자)
   - [팩트] 표시, 시간·장소·주체·수치 명확
   - 출처 인라인: "한국은행이 오늘 14시 발표한 통화정책방향 보고서에 따르면..."

4. 왜 이게 중요한가 (1.5~2분, 600~800자)
   - 시청자 삶과 직접 연결: "여러분 통장에 어떤 영향?"
   - 메모리 [feedback_retention_general_viewer] — 신규 시청자도 진입 가능하게

5. 앞으로 어떻게 될까 (1~1.5분, 400~600자)
   - [예측] 3시나리오 (낙관/중립/비관)
   - 비슷한 과거 사례 1개 비교

6. 지금 당장 할 일 (1분, 400자)
   - 구체 행동 가이드 3가지 (체크리스트)
   - ⚠️ 단정·종목·연령 비중 권유 금지 — 메모리 [feedback_comment_reply_no_advice] 룰 본문에도 적용
   - "본인 위험 성향에 따라" / "전문가 상담 후 결정" 조건부 표현

7. 마무리 + 업데이트 약속 (30~40초, 200~270자)
   - "추가 소식 들어오는 대로 업데이트 영상 올려드릴게요"
   - 클로징 메모리 [feedback_q3_promise_avoidance] 준수 — 약속형 회피
```

**🔴 안전 게이트 (속보 모드 우선 적용)**:
- 13게이트 SSOT 전부 적용 (속보는 압박감 때문에 단정·과장 위험 더 큼 → 표현 점검 강화)
- 모든 [팩트] 수치에 출처 인라인 필수
- "현재까지 확인된 내용입니다" 멘트 본문 1회 이상
- 정치·역사 이슈는 1차 출처 2개 + 추정 표현 강제 (메모리 [feedback_youtube_policy_safety])

산출: `{P}/_script/draft.md` (PD 직접) → `merge_draft.py` 거치지 않고 그대로 사용 가능 (단일 파트)

### 3단계: REVIEW + 확정 (2분 이내)

- script-reviewer 호출 (요약 모드 — 13게이트 + 신규 주장 WebSearch 검증)
- verdict 통과 시 즉시 `finalize.py` → `script.txt`
- verdict 수정 시 1회 리비전, 그 외 PD 직접 정리 (속도 우선)

### 4단계: 쇼츠 1개 (1분 이내)

- 일반 SHORTS 단계와 동일 구조, 단 **1개만** 생성
- 단일 이슈의 가장 자극적인 단면 (수치 1개 + 행동 1개)
- 산출: `{P}/_script/shorts/shorts_01.txt` + `shorts_meta.json`

### 5단계: 풀패키지 출력 (1분 이내)

- `youtube.md` — 디스클레이머 5줄 + 챕터(7개) + 태그 30개 이내 + 해시태그 10~15
- `prompts.json` — 썸네일 (속보 색상 권장: 빨강#E63946 + 검정#1D1D1D + 노랑#FFD60A 강조)
- 제목 권장 패턴 C: `[속보] {발표 주체} {핵심 수치}, {영향}`
  예: `[속보] 한국은행 금리 0.25%p 인상, 우리 대출이자 얼마 오르나`

### 속보 모드 체크리스트
- [ ] 공식 1차 출처 확인 (정부/한은/Fed 등)
- [ ] 2차 출처 1개 이상 크로스체크
- [ ] 수치·날짜·시간 정확
- [ ] "추가 소식 들어오는 대로 업데이트" 멘트 포함
- [ ] 트렌딩 키워드 제목·태그·자막에 반영
- [ ] 시청자 즉시 행동 가이드 3가지 (단, 비중 권유 금지)
- [ ] 제목에 `[속보]` 또는 `[방금발표]` 대괄호 태그
- [ ] AI 디스클레이머 5줄 (속보도 예외 없음)

### 처리 시간 목표 (총 15분)

| 단계 | 목표 시간 |
|---|---|
| 자료 수집 + 크로스체크 | 5분 |
| 단일 DRAFT 작성 | 8분 |
| REVIEW + 확정 | 2분 |
| 쇼츠 1개 + 풀패키지 | 1분 (병렬) |
