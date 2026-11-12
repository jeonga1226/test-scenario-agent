from typing import Literal

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    tc_id: str = Field(description="TC-001 형식, 1부터 순서대로")
    feature: str = Field(description="기능명 (예: 로그인, 회원 검색)")
    title: str = Field(description="테스트 항목")
    precondition: str = Field(description="사전 조건, 없으면 '없음'")
    steps: str = Field(description="1. 2. 3. 번호를 붙인 테스트 절차")
    input_data: str = Field(description="입력값, 없으면 '-'")
    expected: str = Field(description="화면에서 눈으로 확인할 수 있는 예상 결과")
    priority: Literal["상", "중", "하"]


class TestCases(BaseModel):
    cases: list[TestCase]