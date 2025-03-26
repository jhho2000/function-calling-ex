"""
함수 호출 예제를 위한 다양한 함수들을 정의하는 모듈
"""

def get_weather(location: str) -> str:
    """
    주어진 위치의 날씨 정보를 반환합니다.
    
    Args:
        location: 날씨를 조회할 위치
        
    Returns:
        날씨 정보 문자열
    """
    # 실제로는 API를 호출하거나 데이터베이스를 조회하겠지만, 예제이므로 간단히 구현
    weather_data = {
        "서울": "맑음, 22°C",
        "부산": "흐림, 20°C",
        "제주": "비, 18°C",
        "대전": "구름 조금, 23°C",
        "광주": "맑음, 24°C"
    }
    
    return weather_data.get(location, f"{location}의 날씨 정보를 찾을 수 없습니다.")

def calculator(operation: str, a: float, b: float) -> str:
    """
    두 숫자에 대한 기본적인 수학 연산을 수행합니다.
    
    Args:
        operation: 수행할 연산 (더하기, 빼기, 곱하기, 나누기)
        a: 첫 번째 숫자
        b: 두 번째 숫자
        
    Returns:
        연산 결과 문자열
    """
    if operation == "더하기":
        return f"{a} + {b} = {a + b}"
    elif operation == "빼기":
        return f"{a} - {b} = {a - b}"
    elif operation == "곱하기":
        return f"{a} * {b} = {a * b}"
    elif operation == "나누기":
        if b == 0:
            return "0으로 나눌 수 없습니다."
        return f"{a} / {b} = {a / b}"
    else:
        return f"지원하지 않는 연산입니다: {operation}"

def translate(text: str, target_language: str) -> str:
    """
    주어진 텍스트를 대상 언어로 번역합니다.
    
    Args:
        text: 번역할 텍스트
        target_language: 대상 언어
        
    Returns:
        번역된 텍스트
    """
    # 실제로는 번역 API를 호출하겠지만, 예제이므로 간단히 구현
    translation_examples = {
        ("안녕하세요", "영어"): "Hello",
        ("안녕하세요", "일본어"): "こんにちは",
        ("안녕하세요", "중국어"): "你好",
        ("감사합니다", "영어"): "Thank you",
        ("감사합니다", "일본어"): "ありがとうございます",
        ("감사합니다", "중국어"): "谢谢"
    }
    
    return translation_examples.get((text, target_language), f"'{text}'를 {target_language}로 번역할 수 없습니다.")

def add_schedule(date: str, event: str) -> str:
    """
    일정을 추가합니다.
    
    Args:
        date: 일정 날짜 (YYYY-MM-DD 형식)
        event: 일정 내용
        
    Returns:
        일정 추가 결과 메시지
    """
    # 실제로는 데이터베이스에 저장하겠지만, 예제이므로 간단히 구현
    return f"일정이 추가되었습니다: {date}에 {event}"

def recommend_movie(genre: str) -> str:
    """
    주어진 장르의 영화를 추천합니다.
    
    Args:
        genre: 영화 장르
        
    Returns:
        추천 영화 목록
    """
    # 실제로는 데이터베이스나 API를 조회하겠지만, 예제이므로 간단히 구현
    movie_data = {
        "액션": ["다이 하드", "매드 맥스: 분노의 도로", "존 윅"],
        "코미디": ["행오버", "브라이즈메이드", "슈퍼배드"],
        "로맨스": ["노트북", "비포 선라이즈", "어바웃 타임"],
        "SF": ["인터스텔라", "매트릭스", "블레이드 러너 2049"],
        "공포": ["샤이닝", "컨저링", "겟 아웃"]
    }
    
    recommended_movies = movie_data.get(genre, [])
    if recommended_movies:
        return f"{genre} 장르 추천 영화: {', '.join(recommended_movies)}"
    else:
        return f"{genre} 장르의 추천 영화가 없습니다."
