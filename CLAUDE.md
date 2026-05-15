# autoworkers

유튜브 영상 대본 자동 제작 파이프라인. 레퍼런스 수집 → 분석 → 전략 → 대본 작성 → 리뷰까지.

## 사용법

### 채널 만들기
채널 생성 요청 시 **반드시 `.claude/skills/channel-setup/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"채널 만들어줘"        → channel-setup 스킬 로드 → 대화형 채널 생성
```

### 대본 만들기 — 2개 스킬 선택

#### `script-pd` — 레퍼런스 영상 기반 대본 (ETF·교육·심층 시리즈)
대본 제작 관련 요청 시 **반드시 `.claude/skills/script-pd/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"대본 만들어줘"        → SKILL.md 로드 → 상태 감지 → 자동 진행
"이어서 해줘"          → 마지막 상태에서 재개
"대본 다시 써줘"       → 해당 단계만 재실행
```

#### `news-latest-3` — 최신 뉴스 3개 기반 풀패키지 (일일 브리핑·속보)
최신 뉴스 콘텐츠 요청 시 **반드시 `.claude/skills/news-latest-3/SKILL.md`를 먼저 읽고** 그대로 따를 것.
```
"최신뉴스 3"             → SKILL.md 로드 → STEP 1~9 자동 진행
"오늘 경제 뉴스 대본"    → 표준 모드 (롱폼 10~15분 + 쇼츠 3개)
"속보 대본 써줘"         → 속보 모드 (15분 트랙 — 5~8분 + 쇼츠 1개)
"○○ 발표 났는데 대본"   → 속보 모드 자동 진입
```

두 스킬 비교:
- `script-pd` — 레퍼런스 영상(yt-dlp) 분석 필수, 상태머신 7단계, 채널별 차별화 강함
- `news-latest-3` — WebSearch 자료 수집만, 9단계 선형, 쇼츠/속보/색상 매트릭스 자동 적용

**공통 SSOT 공유**:
- `prompts/youtube-policy-gates.md` — 13게이트 정책 안전
- `prompts/seo-titles.md` — 제목 A/B/C 패턴
- `prompts/hook-types.md` — 훅 7유형
- `prompts/thumbnail-design.md` — 색상 심리학 매트릭스
- `prompts/pd-templates.md` — 산출물 포맷
- `prompts/quality-gates.md` — PD 직접 검증

## 프로젝트 구조

```
autoworkers/
├── .claude/
│   ├── skills/script-pd/SKILL.md     # PD 두뇌 (상태머신)
│   ├── skills/channel-setup/SKILL.md # 채널 생성 스킬
│   └── agents/                        # 역할별 에이전트 정의
├── channels/{channel-name}/            # 채널별 설정 + 프로젝트
│   ├── config/                        # 채널 설정 파일
│   │   ├── settings.json              # 채널 식별 (id, name)
│   │   └── profile.md                 # 채널 성격 전체 (장르, 톤, 서사, 관점 등)
│   └── projects/                      # 영상별 작업 폴더
│       └── {project-name}/
│           ├── _refs/                  # 레퍼런스 수집 결과
│           ├── _script/               # 대본 단계 산출물
│           └── output/                # 최종 산출물 (youtube.md, thumbnails/)
├── prompts/                           # 에이전트용 프롬프트
├── scripts/                           # Python 코드
│   ├── collect.py                     # yt-dlp 수집
│   ├── finalize.py                    # draft → script.txt
│   └── src/                           # 유틸리티
└── requirements.txt                   # Python 의존성
```

## 크로스 플랫폼 규칙 (필수)

이 프로젝트는 macOS와 Windows 사용자가 함께 사용한다. **모든 명령어 실행 시 OS를 자동 감지하여 적절한 명령어를 사용할 것.**

### Python 실행
- macOS/Linux: `.venv/bin/python scripts/...`
- Windows: `.venv\Scripts\python scripts/...`

```bash
# macOS/Linux
.venv/bin/python scripts/collect.py --project {project} --channel "{channel}" URL1 URL2

# Windows (cmd/PowerShell)
.venv\Scripts\python scripts/collect.py --project {project} --channel "{channel}" URL1 URL2
```

### pip 실행
- macOS/Linux: `.venv/bin/pip install -U yt-dlp`
- Windows: `.venv\Scripts\pip install -U yt-dlp`

### 파일/디렉토리 조작 — 셸 명령 대신 Python 사용
OS별 셸 명령(`mv`, `rm -r`, `mkdir -p` 등)은 크로스 플랫폼 호환이 안 되므로, **Python으로 대체**한다:

```bash
# mkdir -p 대신
python -c "import os; os.makedirs('path/to/dir', exist_ok=True)"

# mv 대신
python -c "import shutil; shutil.move('src', 'dst')"

# rm -r 대신
python -c "import shutil; shutil.rmtree('path/to/dir')"
```

> **프롬프트/스킬의 셸 명령은 예시일 뿐이다.** 실행 시 반드시 현재 OS에 맞는 명령어를 사용할 것.

## 완료 선언 전 검증 (Quality Gates)

**모든 작업 종료 시 사용자에게 "완료" 보고하기 전에 `prompts/quality-gates.md` SSOT의 5개 게이트를 통과해야 한다.**

### 핵심 룰
1. **에이전트 자가 보고는 검증의 시작이지 끝이 아니다** — PD가 무조건 Grep으로 직접 재검증
2. **검색 패턴은 변형 18개 이상** — 좁은 패턴은 누락 보장
3. **0건 확인 전 "완료" 선언 금지** — 잔존 발견 시 PD 직접 정리 (에이전트 재호출 X)
4. **같은 누락 2회 이상 = 에이전트 신뢰 정지, PD 직접 마무리**

### 자동화 레이어
- **PostToolUse Hook**: `.claude/hooks/verify-consistency.py` — 영상 노출 산출물 변경 시 자동 Grep 알림
- **슬래시 커맨드**: `/verify {프로젝트명}` — 전수 검증 트리거 (`.claude/commands/verify.md`)
- **메모리 룰**: `feedback_verify_before_complete.md` — PD 자율 검증 강제

근거: 2026-05-10 ep07-part3 톤 전환 작업에서 1차 에이전트 "0건 잔존" 보고 → 실제 17건 잔존, 2차도 4건 잔존. "에이전트는 자기 누락을 모른다" 원칙 시스템화.

## 산출물

최종 산출물은 `_script/script.txt`. 이 파일을 영상 제작 사이트에 업로드하면 TTS → 영상 제작이 자동 진행됨.
부가 산출물: `output/youtube.md` (제목/설명/태그), `output/thumbnails/prompts.json` (썸네일 프롬프트).
