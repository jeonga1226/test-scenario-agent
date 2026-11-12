from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from .schemas import TestCase, TestCases 


load_dotenv()
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


# ① State: 그래프 전체가 공유하는 데이터
# TypedDict로 "어떤 값들이 오가는지"를 선언합니다. 프론트로 치면 Redux store의 타입 정의와 같아요.
class State(TypedDict):
    source: str     # 입력: 화면 소스
    features: str   # 결과: 기능 분석
    cases: list[TestCase]


# ② Node: State를 받아서, 바꿀 값만 dict로 돌려주는 함수
# React의 setState({ features })가 일부만 업데이트하는 것과 같은 원리입니다.
def analyze(state: State) -> dict:
    prompt = (
        "다음 화면 소스를 분석해서, 사용자가 테스트해야 할 기능을 정리해줘. "
        "입력 항목, 버튼, 검증 규칙, 오류 메시지를 빠짐없이 적어.\n\n"
        f"{state['source']}"
    )
    result = llm.invoke(prompt) # 초기 State를 넣고
    return {"features": result.content}


# 테스트 케이스 설계 노드
def design_cases(state: State) -> dict:
    prompt = (
        "너는 SI 프로젝트의 테스트 담당자다. 아래 기능 분석과 화면 소스를 보고 단위테스트 케이스를 작성해.\n"
        "- 기능마다 정상 케이스와 예외 케이스(필수값 누락, 잘못된 값, 결과 없음 등)를 포함해\n"
        "- 화면 소스에 구현이 빠져 있더라도, 일반적으로 당연히 기대되는 검증(예: 필수값 체크)은 케이스로 만들어\n"
        "- 예상 결과는 화면에 표시되는 문구나 상태로 구체적으로 적어\n\n"
        f"[기능 분석]\n{state['features']}\n\n"
        f"[화면 소스]\n{state['source']}"
    )
    structured_llm = llm.with_structured_output(TestCases)
    result = structured_llm.invoke(prompt)   # result는 TestCases 객체
    return {"cases": result.cases}


# ③ 그래프 조립: 노드 등록 + Edge(연결선)
def build_graph():
    graph = StateGraph(State)
    graph.add_node("analyze", analyze)
    graph.add_node("design_cases", design_cases)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "design_cases")
    graph.add_edge("design_cases", END)
    return graph.compile() # 최종 State 전체를 받는다
