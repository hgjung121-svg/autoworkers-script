"""Extract key fields from yt-dlp info.json + plain text from VTT."""
import json
import re
import glob
import os

# Key fields to extract from info.json
KEY_FIELDS = [
    "id", "title", "upload_date", "duration", "view_count",
    "like_count", "comment_count", "channel", "uploader",
    "description", "tags", "categories", "thumbnail",
    "average_rating", "chapters", "age_limit",
]


def vtt_to_text(vtt_path):
    """Convert VTT to plain text, dedup identical lines."""
    with open(vtt_path, "r", encoding="utf-8") as f:
        raw = f.read()
    lines = raw.splitlines()
    text_lines = []
    seen_prev = None
    for ln in lines:
        # Skip VTT headers, timestamps, empty, tags
        if not ln.strip():
            continue
        if ln.startswith("WEBVTT") or ln.startswith("Kind:") or ln.startswith("Language:"):
            continue
        if "-->" in ln:
            continue
        if re.match(r"^\d+$", ln.strip()):
            continue
        # Remove VTT inline tags like <c>, <00:00:00.000>
        cleaned = re.sub(r"<[^>]+>", "", ln).strip()
        if not cleaned:
            continue
        if cleaned == seen_prev:
            continue
        text_lines.append(cleaned)
        seen_prev = cleaned
    return "\n".join(text_lines)


def process():
    info_files = sorted(glob.glob("*.info.json"))
    results = []
    for info_file in info_files:
        with open(info_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        vid = data.get("id")
        slim = {k: data.get(k) for k in KEY_FIELDS}
        # Shorten description for scan
        desc = slim.get("description") or ""
        slim["description_preview"] = desc[:400]
        slim["description_length"] = len(desc)
        slim.pop("description")
        # Subtitle
        vtt_path = f"{vid}.ko.vtt"
        if os.path.exists(vtt_path):
            subtitle = vtt_to_text(vtt_path)
            slim["subtitle_length"] = len(subtitle)
            slim["subtitle_preview"] = subtitle[:600]
            # Save cleaned subtitle to .txt
            out_txt = f"{vid}.subtitle.txt"
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write(subtitle)
        results.append(slim)

    # Write summary
    with open("_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Markdown digest
    lines = ["# 5 영상 메타데이터 요약\n"]
    for r in results:
        lines.append(f"## {r.get('title')}")
        lines.append(f"- ID: `{r.get('id')}`")
        lines.append(f"- 업로드: {r.get('upload_date')} / 길이: {r.get('duration')}초")
        lines.append(f"- 조회수: {r.get('view_count'):,} / 좋아요: {r.get('like_count')} / 댓글수: {r.get('comment_count')}")
        lines.append(f"- 채널: {r.get('channel')}")
        lines.append(f"- 태그: {r.get('tags')}")
        lines.append(f"- 설명 미리보기: {r.get('description_preview')[:200]}")
        lines.append(f"- 자막 길이: {r.get('subtitle_length')}자")
        lines.append("")
    with open("_digest.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK")
    print(f"Processed {len(results)} videos")


if __name__ == "__main__":
    process()
