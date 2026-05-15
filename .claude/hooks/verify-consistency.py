"""PostToolUse hook: 영상 노출 산출물 변경 후 자동 톤 일관성 검증.

검증 대상 (Edit / Write 매처):
- channels/*/projects/*/_script/script.txt
- channels/*/projects/*/_script/script-oneline.txt
- channels/*/projects/*/_script/concept.md
- channels/*/projects/*/_script/hook-intro.md
- channels/*/projects/*/output/youtube.md
- channels/*/projects/*/output/thumbnails/prompts.json

검증 패턴 (메모리 룰 + prompts/quality-gates.md 기반):
1. 톤 전환 잔존 (보충편/답변 영상의 댓글자 지목 표현)
2. 단정 표현 (게이트 4 — YMYL 금융정보)
3. AI 도입 패턴 (게이트 1)

발견 시 stderr로 경고 출력 → Claude 다음 응답에 자동 첨부.
hookSpecificOutput.permissionDecision은 사용 안 함 (차단 X, 알림만).
"""
import sys
import json
import re
import os
import subprocess

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = data.get("tool_input") or {}
fp = tool_input.get("file_path", "")
fp_norm = fp.replace("\\", "/")

# 검증 대상 파일 패턴
target_patterns = [
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/script\.txt$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/script-oneline\.txt$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/concept\.md$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/hook-intro\.md$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/output/youtube\.md$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/output/thumbnails/prompts\.json$",
]

is_target = any(re.search(p, fp_norm) for p in target_patterns)
if not is_target:
    sys.exit(0)

# 파일이 실제로 존재해야 검증 가능
if not os.path.exists(fp):
    sys.exit(0)

# 파일 내용 읽기
try:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
except Exception:
    sys.exit(0)

# 검증 패턴 매트릭스
violations = []

# 1. 톤 전환 잔존 (보충편/답변 영상)
tone_patterns = [
    r"비판자",
    r"비판\s?댓글",
    r"한\s분이",
    r"댓글창",
    r"그\s댓글",
    r"비판\s?받",
    r"비판\s?들",
    r"비판\s?정면",
    r"비판\s?회수",
    r"비판자에",
    r"비판\s?핵심",
    r"비판\s?모드",
    r"비판\s?영상",
    r"비판\s?답변",
    r"비판\s?인정",
    r"비판\s?인용",
]
for pattern in tone_patterns:
    matches = re.findall(pattern, content)
    if matches:
        violations.append(f"톤 전환 잔존: '{pattern}' {len(matches)}건")
        break  # 첫 패턴만 보고 (전체 매핑은 quality-gates.md 참조)

# 2. 단정 표현 (게이트 4 — YMYL)
ymyl_patterns = [
    (r"무조건\s?(?:사|팔|오른|내려)", "단정 표현 (무조건 + 매수/매도)"),
    (r"100%\s?수익", "단정 표현 (100% 수익 보장)"),
    (r"확정\s?수익", "단정 표현 (확정 수익)"),
    (r"반드시\s?(?:오른|내려|수익)", "단정 표현 (반드시 + 결과)"),
    (r"절대\s?(?:사|팔)", "단정 표현 (절대 + 매수/매도)"),
]
for pattern, label in ymyl_patterns:
    if re.search(pattern, content):
        violations.append(f"YMYL 위반: {label}")

# 3. AI 도입 패턴 (게이트 1)
ai_patterns = [
    (r"^오늘은\s+", "AI 도입 패턴 ('오늘은~')"),
    (r"결론적으로\s+", "AI 결론 패턴 ('결론적으로~')"),
    (r"알아보겠습니다", "AI 도입 패턴 ('알아보겠습니다')"),
]
for pattern, label in ai_patterns:
    if re.search(pattern, content, re.MULTILINE):
        violations.append(f"AI 패턴 위반: {label}")

# 위반 발견 시 stderr 경고
if violations:
    msg = (
        f"\n[verify-consistency Hook] {fp_norm}\n"
        + "\n".join(f"  ⚠️ {v}" for v in violations)
        + "\n\n→ prompts/quality-gates.md 게이트 1~3 점검 필요. "
        "PD가 직접 Grep으로 재검증 후 정밀 수정 권장.\n"
    )
    # PostToolUse는 stderr가 다음 Claude 응답에 추가 컨텍스트로 들어감
    sys.stderr.write(msg)
    sys.exit(2)  # exit 2 = stderr 메시지를 Claude에 첨부

sys.exit(0)
