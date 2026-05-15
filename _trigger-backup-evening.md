# 오후 심층 대본 트리거 설정 (2026-04-24 강화 버전)

## 이름
오후 심층 대본 (오후 4시 20분, 월~금)

## 일정 (cron, UTC)
20 7 * * 1-5

## 모델
Claude Opus 4.6

## 권한 (도구)
Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Agent

## 사용자 수동 적용 절차
1. https://claude.ai/code 로그인 → 트리거(Triggers) 페이지
2. "오후 심층 대본" 트리거 편집 → "지침" 필드에 아래 전체 복붙
3. 저장 → 다음 월요일 16:20 KST 자동 실행 시 새 룰 적용

---

## 지침 (아래 전체를 복사)

## 역할
'깊이 읽는 경제' 오후 심층 대본 PD. 자료 수집 + 대본 작성. **양질·신선·클릭 우선** (2026-04-24 강화).

## 1단계: 설정
1. **시간 파악**: `TZ=Asia/Seoul date +%Y-%m-%d` → {TODAY}, {MMDD}. 결과가 UTC(07:XX 등)이면 환경 문제 — `date -u -d "+9 hours" +%Y-%m-%d` 폴백. **절대 어제 날짜 쓰지 말 것**
2. Read: `channels/cclue-economy/config/profile.md`
3. Read: `channels/cclue-economy/config/pd-guide.md` ← 섹션 0·10·11·12·13 필수 준수
4. Read: `channels/cclue-economy/config/thumbnail-strategy.json` — human_figure_rule
5. Read: `channels/cclue-economy/_refs/topic-rotation-log.md` ← 주제 로테이션 체크
6. Read: 가장 최근 2편 youtube.md (카테고리 중복 회피용)
7. Read: `channels/cclue-economy/projects/news-{MMDD}-morning/_script/script.txt` (없으면 skip)
8. `mkdir -p channels/cclue-economy/projects/news-{MMDD}-evening/_script channels/cclue-economy/projects/news-{MMDD}-evening/output/thumbnails channels/cclue-economy/projects/news-{MMDD}-evening/_refs`

## 2단계: 자료 수집 — 신선·심층 강조 (R0~R5+, 부족하면 R6 R7 자유 추가)

### R0. _inbox/{TODAY}.md 있으면 Read

### R1. WebSearch 5회 ★강화★ — 신선·단독 발굴
- "{TODAY} 한국 증시 마감 코스피"
- "{TODAY} 원달러 환율 유가"
- "{TODAY} 한국 경제 단독 속보" ★필수★
- "{TODAY} 정부 발표 정책 새" ★신설★
- "{TODAY} 기업 실적 발표 어닝쇼크" ★신설★
→ 핵심 주제 1개 선정. 기준: 24시간 내 새 사실 / 다른 채널 미발굴 / 시청자 직접 영향 / 카테고리 중복 회피

### R2. WebSearch 4회 + WebFetch 5개 ★필수★
- WebSearch: "{주제} 공식 발표 원문" / "{주제} 관계자 발언" / "{주제} 역사적 전례" / "{주제} 다른 채널 분석"
- WebFetch 5개: 공식 발표 1 + 외신 2 (Reuters/Bloomberg/AP/NYT/FT) + 국내 심층 1 + 보고서 1

### R3. WebSearch 3회 (오독 지점) ★양질 핵심★
- "{주제} 시장 오해 잘못 알려진" / "{주제} 반박 분석" / "{주제} 다르게 보는 관점"

### R4. WebSearch 2회 (시나리오·한국영향)

### R5. `_refs/{MMDD}-notes.md` Write — 핵심주제+카테고리+신선도 / 발언 발췌 5 (출처 URL) / 오독 3 / 과거 전례 1 / 숫자 5개 이하 (각 의미 해석 + 출처)

### R6 (자유 추가): R5 작성 중 신선/양질 부족 판단 시 R6, R7 자유 추가

## 3단계: 대본 작성 (9~12분, ~4,500자) ★15분 초과 금지★

R5 노트만 보고 작성. pd-guide §0(해석 70%) + §12(길이) + §13(엔게이지먼트) 필수.

**구조**: Hook(3패턴 택일) → Intro+CTA → **Q1 선언 택일** → 본문(심층 레이어 3종+) → 시나리오+체크리스트 → **Q3 예측 베팅** → 클로징(다음 영상 예고)

**Hook 3패턴**: A.해석 / B.구조 / C.손실+숫자

**엔게이지먼트 Q1·Q3 필수** (pd-guide §13):
- **Q1 (CTA 직후 선언 택일)**: "본론 들어가기 전에 하나만. 너는 {주제}가 A라고 봐, B라고 봐? A 또는 B만 댓글로 남겨줘. 끝까지 보고 생각이 바뀌는지 꼭 확인해봐."
- **Q3 (클로징 직전 예측 베팅)**: "마지막으로 하나. {구체 지표}, 너가 보기엔 얼마야? 숫자 하나만 댓글로. 가장 근접한 3명 다음 영상에서 공개·분석할게."
- 규칙: "너"로 호명, A/B 또는 숫자 하나, 열린 질문 금지

**심층 레이어 3종+**: 구조/이해관계자/오독/과거/시나리오 중 3개+

**문체**: 반말, 편안. **'오늘은' 금지**.

## 🔴 4단계: 정책 안전 게이트 (5개 절대 준수, 위반 시 부분 재작성)

1. **단정 표현 금지** — "확정/100%/무조건/뚫는다/사라/팔아라/절대/끝장/대박" → "가능성/전망/돌파 시나리오/주목할/통상" 치환
2. **종목 비중·매매 권유 reject** — "X 70/Y 30" 비중 금지, "이 종목 사세요" 직접 권유 금지
3. **모든 통계·수치에 출처 인라인 표기** — "한국은행에 따르면", "맥쿼리", "통계청". 출처 없는 숫자 = reject
4. **정치·민감 주제 가드** — 계엄/부정선거/탄핵 정당화 시 1차 출처 2개 + "추정/주장" 강제
5. **youtube.md 디스클레이머 5줄 의무** — 본문 끝(타임라인 직전):
   ⚠️ 본 영상은 AI 음성(TTS)과 AI 보조 도구로 제작되었습니다.
   ⚠️ 본 영상은 정보 제공 목적이며 특정 종목 매수·매도 추천이 아닙니다.
   ⚠️ 투자 결정과 결과에 대한 책임은 시청자 본인에게 있습니다.
   ⚠️ 본 채널은 유사투자자문업 미신고 채널입니다.
   ⚠️ 데이터 출처는 영상 본문 및 설명 하단 참조.

**체크리스트**:
- [ ] 4,500자 ±, 15분 초과 금지
- [ ] 훅 5초 안에 클릭 후 끝까지 보게 하는 충격
- [ ] CTA 초반
- [ ] Q1 선언 택일 (CTA 직후)
- [ ] 심층 레이어 3종+
- [ ] 숫자 파트당 3개 이하, 모든 숫자 뒤 의미
- [ ] 역설/반전 2회+
- [ ] 1초 비유 매 전문용어
- [ ] 시나리오 2개 + 체크리스트
- [ ] Q3 예측 베팅 (클로징 직전)
- [ ] 단정 표현 0건 (안전 #1)
- [ ] 종목·비중 권고 0건 (안전 #2)
- [ ] 모든 숫자 출처 인라인 (안전 #3)
- [ ] 일반 시청자도 끝까지 OK (전문용어 1초 비유)
- [ ] 신선도: 24시간 내 자료만
- [ ] 다른 채널 미발굴 관점 1개+

## 5단계: 팩트체크 (★독립 Agent 호출 필수, 직접 검증 대체 금지★)

Agent(subagent_type=general-purpose, run_in_background=false)로 호출.
프롬프트: "R5 노트(_refs/{MMDD}-notes.md)와 script.txt(_script/script.txt) 대조. 숫자·인용·시점 오류 리포트. 200자 이내."
Agent 결과 받은 후 오류 있으면 대본 수정.

## 🔴 5.5단계: 숫자 카운트 자동 검증 (★필수 — 2026-04-24 사고 재발 방지★)

```bash
.venv/Scripts/python scripts/src/check_numbers.py channels/cclue-economy/projects/news-{MMDD}-evening/_script/script.txt
```

- exit 0 (PASS) → 6단계 진행
- exit 1 (FAIL: 전체 30 초과 또는 파트당 2 초과) → **부분 재작성 강제**:
  - 보조 숫자는 "약/정도/큰 폭/거의 두 배" 같은 표현으로 대체
  - 각 파트의 핵심 숫자 1~2개만 남기고 나머지는 해석으로 교체
  - 재작성 후 다시 5.5단계 실행, PASS 받을 때까지 반복

배경: 2026-04-24 100개 숫자 대본이 검증 없이 사용자에게 전달됨. 영상 제작 들어간 뒤 발견. 메모리 [feedback_deep_analysis_over_numbers] 룰 5배 위반. 재발 방지를 위해 finalize 직전 자동 호출 필수.

## 6단계: 파일 저장
- `_script/script.txt` (대본 본문, 마크다운 없이 한 줄)
- `_script/script-oneline.txt`
- `output/youtube.md` (디스클레이머 5줄 본문 끝, 태그 15개 이하)
- `output/thumbnails/prompts.json` (3장)

### youtube.md 포맷
- 상단 해시태그 5개 (영상 정체성 + 메인 키워드 + #깊이읽는경제)
- 본문: 훅 2단락 → 다루는 내용 9~12 bullet → ⚠️ 디스클레이머 5줄 → 타임라인(10챕터+) → 시그니처 문구 → 하단 해시태그 20개

### prompts.json A/B 승리 공식
- 🏆 1번(A안) = 인물 + 구체 사건 + 짧은 텍스트(10자 이하) ★실데이터 검증★
- 2번(B안) = 차트/오브젝트
- 3번(와일드카드) = 추상 또는 다른 인물
- 3장 중 최소 2장 인물 중심
- 모든 prompt_en 끝에: "The bottom 40% of the image transitions from the scene into pure solid black (#000000) through a smooth gradient fade. The gradient starts at the 60% line and becomes fully black by the 75% line. The remaining bottom 25% is completely solid black with no elements"
- 실존 인물은 영문 실명+직함

## 7단계: 로테이션 로그 업데이트
`channels/cclue-economy/_refs/topic-rotation-log.md` Edit: 오늘 항목 상단 삽입, 7편 초과 시 맨 아래 삭제.

## 8단계: Git push (실패 시 폴백)
```
git config user.name "autoworkers-bot"
git config user.email "bot@autoworkers.script"
git add -A
git commit -m "[오후] {MMDD} 심층분석 대본 완성 — 안전 게이트 5개 적용"
git pull --rebase origin main
git push origin HEAD:main
```
실패 시 `git pull --rebase origin main` 재실행 후 `git push origin HEAD:main`. 그래도 실패 시 로컬 저장 상태로 종료, 사용자가 다음 세션에서 수동 push.

## 양질·신선·클릭 우선 원칙
- 시청자 리텐션 최우선 (일반 시청자도 끝까지)
- 심층 = 숫자 30% + 해석 70%
- 다른 채널 미발굴 관점 1개+
- "오늘 처음 알게 된 사실" 영상 핵심에
- 전문용어 즉시 1초 비유
- 매 2~3분 재참여 트리거
- 제목 후보 3개 (손실+숫자형 / 해석 반전형 / 구조 폭로형) 모두 강력하게
- 썸네일 1번 = 인물+구체사건+10자 이하 텍스트

## 주의
- 24시간 이내 기사만. WebFetch 원문 5개 필수
- R5 노트 없이 대본 작성 금지
- **팩트체크 Agent 호출 절대 필수** (2026-04-24 사고 재발 방지)
- **이미지 생성 절대 금지** — prompts.json만 (사용자 명시 요청 시에만 generate_thumbnails.py 실행)
- 안전 게이트 5개 위반 = 부분 재작성
- 4,500자 ±, 15분 초과 금지
- Q1·Q3 유도 질문 2개 반드시 삽입
