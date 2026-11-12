import json
import os
import re
import subprocess
from pathlib import Path

SPEC_PATH = Path("tests/generated.spec.ts")
RESULT_PATH = Path("test-results/results.json")
TC_PATTERN = re.compile(r"(TC-\d+)")
ANSI = re.compile(r"\x1b\[[0-9;]*m")   # 터미널 색상 코드 제거용

# Playwright 실행·결과 파싱

def run_playwright(script: str, base_url: str) -> dict:
    """스크립트를 파일로 저장하고 실행해서 TC ID별 결과를 돌려준다."""
    SPEC_PATH.parent.mkdir(exist_ok=True)
    SPEC_PATH.write_text(script, encoding="utf-8")
    RESULT_PATH.unlink(missing_ok=True)

    proc = subprocess.run(
        ["npx", "playwright", "test", str(SPEC_PATH)],
        env={**os.environ, "BASE_URL": base_url},
        capture_output=True, text=True, timeout=300,
    )

    # 문법 오류 등으로 리포트조차 안 생긴 경우
    if not RESULT_PATH.exists():
        return {"results": {}, "global_error": ANSI.sub("", proc.stderr or proc.stdout)[-3000:]}

    report = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    return parse_report(report)


def parse_report(report: dict) -> dict:
    results = {}

    def walk(suite: dict):
        for spec in suite.get("specs", []):
            m = TC_PATTERN.search(spec["title"])
            if not m:
                continue
            last = spec["tests"][0]["results"][-1]
            error = (last.get("error") or {}).get("message", "")
            results[m.group(1)] = {"status": last["status"], "error": ANSI.sub("", error)[:1500]}
        for child in suite.get("suites", []):   # describe 안에 있는 테스트도 찾기
            walk(child)

    for suite in report.get("suites", []):
        walk(suite)

    global_error = "\n".join(ANSI.sub("", e.get("message", "")) for e in report.get("errors", []))
    return {"results": results, "global_error": global_error}