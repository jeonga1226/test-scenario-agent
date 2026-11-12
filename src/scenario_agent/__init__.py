import json
from pathlib import Path

from .graph import build_graph


def main() -> None:
    app = build_graph()
    source = Path("sample_app/index.html").read_text(encoding="utf-8")

    result = app.invoke({"source": source})

    for c in result["cases"]:
        print(f"{c.tc_id} [{c.priority}] {c.feature} | {c.title}")
        print(f"    → {c.expected}")

    # 다음 단계에서 재사용하려고 파일로 저장
    data = [c.model_dump() for c in result["cases"]]
    Path("cases.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n총 {len(data)}개 케이스 → cases.json 저장")