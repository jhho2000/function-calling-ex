"""
LLM을 사용하여 사용자 입력에 따라 다른 함수를 호출하는 예제 프로그램
"""

import json
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import openai

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 함수 모듈 가져오기
from functions import get_weather, calculator, translate, add_schedule, recommend_movie

# 함수 정의 (OpenAI function calling 형식)
function_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "특정 도시의 날씨 정보를 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "날씨를 조회할 도시 이름 (예: 서울, 부산, 제주)"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "두 숫자 간의 기본적인 수학 연산을 수행합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "수행할 연산 (더하기, 빼기, 곱하기, 나누기)",
                        "enum": ["더하기", "빼기", "곱하기", "나누기"]
                    },
                    "a": {
                        "type": "number",
                        "description": "첫 번째 숫자"
                    },
                    "b": {
                        "type": "number",
                        "description": "두 번째 숫자"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate",
            "description": "텍스트를 다른 언어로 번역합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "번역할 텍스트"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "대상 언어 (영어, 일본어, 중국어)",
                        "enum": ["영어", "일본어", "중국어"]
                    }
                },
                "required": ["text", "target_language"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_schedule",
            "description": "특정 날짜에 일정을 추가합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "일정 날짜 (YYYY-MM-DD 형식)"
                    },
                    "event": {
                        "type": "string",
                        "description": "일정 내용"
                    }
                },
                "required": ["date", "event"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_movie",
            "description": "특정 장르의 영화를 추천합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "영화 장르 (액션, 코미디, 로맨스, SF, 공포)",
                        "enum": ["액션", "코미디", "로맨스", "SF", "공포"]
                    }
                },
                "required": ["genre"]
            }
        }
    }
]

def llm_function_call_decision(user_input: str) -> Optional[Dict[str, Any]]:
    """
    LLM을 사용하여 사용자 입력을 분석하고 호출할 함수와 인자를 결정합니다.
    
    Args:
        user_input: 사용자 입력 문자열
        
    Returns:
        함수 호출 정보 딕셔너리 또는 None
    """
    try:
        # OpenAI API 호출
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # function calling을 지원하는 모델
            messages=[
                {"role": "system", "content": "사용자의 요청을 분석하여 적절한 함수를 호출하세요."},
                {"role": "user", "content": user_input}
            ],
            tools=function_definitions,
            tool_choice="auto"  # 자동으로 적절한 함수 선택
        )
        
        # 응답에서 함수 호출 정보 추출
        message = response.choices[0].message
        
        # 함수 호출이 있는 경우
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            return {
                "function": function_name,
                "arguments": arguments
            }
        
        return None
    
    except Exception as e:
        print(f"LLM 호출 중 오류 발생: {str(e)}")
        return None

def call_function(function_name: str, args: Dict[str, Any]) -> str:
    """
    함수 이름과 인자를 받아 해당 함수를 호출합니다.
    
    Args:
        function_name: 호출할 함수 이름
        args: 함수 인자 딕셔너리
        
    Returns:
        함수 호출 결과
    """
    function_mapping = {
        "get_weather": get_weather,
        "calculator": calculator,
        "translate": translate,
        "add_schedule": add_schedule,
        "recommend_movie": recommend_movie
    }
    
    if function_name in function_mapping:
        try:
            # 함수 호출 및 결과 반환
            return function_mapping[function_name](**args)
        except Exception as e:
            return f"함수 호출 중 오류 발생: {str(e)}"
    else:
        return "지원하지 않는 함수입니다."

def print_function_call_info(function_info: Dict[str, Any]) -> None:
    """
    함수 호출 정보를 JSON 형식으로 출력합니다.
    
    Args:
        function_info: 함수 호출 정보 딕셔너리
    """
    print("\n[함수 호출 정보]")
    print(json.dumps(function_info, ensure_ascii=False, indent=2))
    print()

def print_help() -> None:
    """도움말 메시지를 출력합니다."""
    print("\n=== 사용 가능한 명령어 예시 ===")
    print("1. 날씨 조회: '서울의 날씨 어때?', '부산 날씨 알려줘'")
    print("2. 계산: '10과 20 더하기 계산해줘', '5에서 3 빼기'")
    print("3. 번역: '안녕하세요를 영어로 번역해줘'")
    print("4. 일정 추가: '2023-04-15에 팀 미팅 일정 추가해줘'")
    print("5. 영화 추천: '액션 영화 추천해줘', 'SF 영화 뭐가 있어?'")
    print("6. 종료: '종료', '끝', 'exit', 'quit'")
    print("==============================\n")

def main():
    """메인 함수"""
    print("=== LLM 기반 함수 호출 예제 프로그램 ===")
    print("사용자 입력에 따라 LLM이 적절한 함수를 결정하여 호출하는 예제입니다.")
    print("'도움말'을 입력하면 사용 가능한 명령어를 볼 수 있습니다.")
    print("'종료'를 입력하면 프로그램이 종료됩니다.")
    print("=========================================\n")
    
    # OpenAI API 키 확인
    if not openai.api_key:
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("'.env' 파일을 생성하고 'OPENAI_API_KEY=your_api_key'를 추가하세요.")
        return
    
    while True:
        # 사용자 입력 받기
        user_input = input("명령을 입력하세요: ")
        
        # 종료 명령 처리
        if user_input.lower() in ['종료', '끝', 'exit', 'quit']:
            print("프로그램을 종료합니다.")
            break
            
        # 도움말 명령 처리
        if user_input.lower() in ['도움말', 'help', '?']:
            print_help()
            continue
        
        # LLM을 사용하여 함수 호출 결정
        function_info = llm_function_call_decision(user_input)
        
        if function_info:
            # 함수 호출 정보 출력
            print_function_call_info(function_info)
            
            # 함수 호출 및 결과 출력
            function_name = function_info["function"]
            arguments = function_info["arguments"]
            result = call_function(function_name, arguments)
            print(f"[결과] {result}\n")
        else:
            print("입력을 이해할 수 없거나 적절한 함수를 찾을 수 없습니다. '도움말'을 입력하여 사용 가능한 명령어를 확인하세요.\n")

if __name__ == "__main__":
    main()
