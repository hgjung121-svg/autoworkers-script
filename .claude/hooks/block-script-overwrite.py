"""PreToolUse hook: Write 도구로 영상 제작 산출물 통째 덮어쓰기를 차단.

차단 대상 4종:
- channels/*/projects/*/_script/script.txt
- channels/*/projects/*/_script/script-oneline.txt
- channels/*/projects/*/output/youtube.md
- channels/*/projects/*/output/thumbnails/prompts.json

Edit는 차단하지 않음 (부분 수정 허용).
"""
import sys
import json
import re

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

fp = (data.get("tool_input") or {}).get("file_path", "")
fp_norm = fp.replace("\\", "/")

patterns = [
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/script\.txt$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/_script/script-oneline\.txt$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/output/youtube\.md$",
    r"(?:^|/)channels/[^/]+/projects/[^/]+/output/thumbnails/prompts\.json$",
]

for p in patterns:
    if re.search(p, fp_norm):
        out = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "영상 제작 산출물(script.txt / script-oneline.txt / "
                    "output/youtube.md / output/thumbnails/prompts.json) "
                    "통째 Write 차단. Edit로 부분 수정하거나 *-v2 별도 파일로 "
                    "작업 후 사용자 승인 시에만 본 파일 교체하세요."
                ),
            }
        }
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.exit(0)

sys.exit(0)
