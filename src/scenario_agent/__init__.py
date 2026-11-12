import json
from pathlib import Path

from .graph import build_graph


def main() -> None:
    APP_DIR = Path("/Users/jeonga/workspace/kosa-frontend/employee-chatbot")

    app = build_graph()
    source = (APP_DIR / "src/pages/LoginPage.tsx").read_text(encoding="utf-8")

    result = app.invoke({"source": source, "base_url": "http://localhost:5173"})

    if result["global_error"]:
        print("스크립트 실행 실패:\n", result["global_error"])
        return

    for c in result["cases"]:
        r = result["results"].get(c.tc_id, {"status": "미실행", "error": ""})
        mark = "✅" if r["status"] == "passed" else "❌"
        print(f"{mark} {c.tc_id} {c.title}")
        if r["error"]:
            print("    ", r["error"].splitlines()[0])