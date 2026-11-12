from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


# ① State: 그래프 전체가 공유하는 데이터
# TypedDict로 "어떤 값들이 오가는지"를 선언합니다. 프론트로 치면 Redux store의 타입 정의와 같아요.
class State(TypedDict):
    source: str     # 입력: 화면 소스
    features: str   # 결과: 기능 분석
    summary: str    # 결과: 기능 분석 요약


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


# analyze가 State에 넣어둔 features를 읽어서 요약
def summarize(state: State) -> dict:
    prompt = (
        "다음 기능 분석 결과를 핵심 기능 위주로 5줄 이내로 요약해줘.\n\n"
        f"{state['features']}"
    )
    result = llm.invoke(prompt)
    return {"summary": result.content}


# ③ 그래프 조립: 노드 등록 + Edge(연결선)
def build_graph():
    graph = StateGraph(State)
    graph.add_node("analyze", analyze)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", END)
    return graph.compile() # 최종 State 전체를 받는다