"""대본 숫자 카운트 검증 — 정책 안전 게이트

오후 심층/주간 대본의 숫자 사용량이 가이드라인 한도를 넘는지 자동 검증.

룰 (메모리 feedback_deep_analysis_over_numbers 2026-04-24 강화):
- 전체 영상 30개 이하 (4,500자 기준)
- 한 파트(빈 줄로 구분) 2개 이하

사용:
  python scripts/src/check_numbers.py path/to/script.txt
  → exit 0: 통과
  → exit 1: 위반 (위반 라인 + 카운트 출력)
"""

import argparse
import re
import sys
from pathlib import Path

# Windows cp949 인코딩 회피 — UTF-8 강제
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass

# 의미 있는 숫자 패턴 (통계·수치)
# - 정수/소수 + 단위 또는 % 또는 단독 숫자
# 제외:
# - 영상 길이 시간(0:00, 12:30 같은 타임라인)
# - 챕터 번호("1단락", "1번째")는 카운트 — 사실상 수치적 의미 없으나 보수적으로
NUMBER_PATTERN = re.compile(
    r'\b\d+(?:[\.,]\d+)?(?:\s*(?:%|퍼센트|포인트|조|억|만|천|원|달러|배|개|회|위|위안|엔|년|월|일|분|초|시|분기|시간|개월|주))?\b'
    r'|\b\d+(?:[\.,]\d+)?\b'
)

# 단순 카운트 제외 패턴 (false positive 방지)
EXCLUDE_PATTERNS = [
    re.compile(r'^\d+\s*단계$'),       # "1단계" 등 절차 번호
    re.compile(r'^\d+\s*번째$'),       # "1번째" 등 순서
    re.compile(r'^[A-Z]\d+$'),         # "Q1", "Q3" 등 질문 라벨
]

# 한도
TOTAL_LIMIT = 30
PART_LIMIT = 2


def count_numbers(text: str) -> list[str]:
    """텍스트에서 의미 있는 숫자 토큰 추출."""
    matches = NUMBER_PATTERN.findall(text)
    # 빈 매치 제거
    return [m.strip() for m in matches if m.strip() and m.strip() != '']


def split_parts(text: str) -> list[str]:
    """대본을 파트 단위로 분리 (빈 줄 기준)."""
    parts = re.split(r'\n\s*\n', text)
    return [p.strip() for p in parts if p.strip()]


def check_script(script_path: Path) -> dict:
    """대본 검증 결과 반환."""
    text = script_path.read_text(encoding='utf-8')
    parts = split_parts(text)

    total_numbers = count_numbers(text)
    total_count = len(total_numbers)

    part_results = []
    violations = []

    for i, part in enumerate(parts, 1):
        part_numbers = count_numbers(part)
        part_count = len(part_numbers)
        part_results.append({
            'part_no': i,
            'count': part_count,
            'numbers': part_numbers,
            'preview': part[:60].replace('\n', ' ') + ('...' if len(part) > 60 else ''),
        })
        if part_count > PART_LIMIT:
            violations.append(f"파트 {i}: {part_count}개 (한도 {PART_LIMIT}개 초과)")

    if total_count > TOTAL_LIMIT:
        violations.insert(0, f"전체: {total_count}개 (한도 {TOTAL_LIMIT}개 초과)")

    return {
        'script_path': str(script_path),
        'total_count': total_count,
        'total_limit': TOTAL_LIMIT,
        'part_limit': PART_LIMIT,
        'parts': part_results,
        'violations': violations,
        'passed': len(violations) == 0,
    }


def print_report(result: dict, verbose: bool = False) -> None:
    """검증 결과 출력."""
    status = "✅ PASS" if result['passed'] else "❌ FAIL"
    print(f"{status} — {result['script_path']}")
    print(f"전체 숫자: {result['total_count']}개 (한도 {result['total_limit']})")
    print(f"파트당 한도: {result['part_limit']}개")
    print()

    if verbose or not result['passed']:
        print("파트별 카운트:")
        for p in result['parts']:
            mark = '⚠️ ' if p['count'] > result['part_limit'] else '   '
            print(f"  {mark}파트 {p['part_no']}: {p['count']}개 — {p['preview']}")
            if verbose and p['numbers']:
                print(f"        숫자: {', '.join(p['numbers'][:10])}{' ...' if len(p['numbers']) > 10 else ''}")
        print()

    if result['violations']:
        print("위반 사항:")
        for v in result['violations']:
            print(f"  ❌ {v}")
        print()
        print("권고:")
        print("  - 보조 숫자는 '약/정도/큰 폭/거의 두 배' 같은 표현으로 대체")
        print("  - 핵심 숫자만 남기고 나머지는 해석으로 교체")
        print("  - 메모리 [feedback_deep_analysis_over_numbers] 참조")


def main() -> int:
    parser = argparse.ArgumentParser(
        description='대본 숫자 카운트 검증 (전체 30개 이하 + 파트당 2개 이하)'
    )
    parser.add_argument('script_path', help='검증할 script.txt 경로')
    parser.add_argument('-v', '--verbose', action='store_true', help='파트별 숫자 목록 출력')

    args = parser.parse_args()

    script_path = Path(args.script_path)
    if not script_path.exists():
        print(f"ERROR: 파일 없음 — {script_path}")
        return 2

    result = check_script(script_path)
    print_report(result, verbose=args.verbose)

    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
