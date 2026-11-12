from pathlib import Path

from .graph import build_graph


def main() -> None:
    app = build_graph()
    source = Path("sample_app/index.html").read_text(encoding="utf-8")

    result = app.invoke({"source": source})
    print(result["features"])
    # # invoke 대신 stream: 노드가 하나 끝날 때마다 결과를 하나씩 돌려줌
    # for step in app.stream({"source": source}, stream_mode="updates"):
    #     for node_name, output in step.items():
    #         print(f"===== [{node_name}] 완료 =====")
    #         print(output)
    
    