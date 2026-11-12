from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    source = Path("sample_app/index.html").read_text(encoding="utf-8")

    prompt = (
        "다음 화면 소스를 분석해서, 사용자가 테스트해야 할 기능을 정리해줘. "
        "입력 항목, 버튼, 검증 규칙, 오류 메시지를 빠짐없이 적어.\n\n"
        f"{source}"
    )
    result = llm.invoke(prompt)
    print(result.content)