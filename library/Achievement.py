from typing import Literal, TypedDict, Dict, cast

ACHIEVEMENT_AREA = Literal[
    'normal',
    'speak',
    'ac',
    'wallet',
    'gamble',
    'fight',
    'tropy'
]

class AchievementContent(TypedDict):
    achievement_area:ACHIEVEMENT_AREA
    name:str
    id:int
    description:str
    plus_description:str
    required:int | float | Dict[str, int | float] | None
    
class Achievement():
    ping: AchievementContent = {
        'achievement_area': 'normal',
        'name': '핑!',
        'id': 1,
        'description': "봇의 핑을 확인해보세요.",
        'plus_description': "찌릿찌릿",
        'required': None
    }
    quizquiz: AchievementContent = {
        'achievement_area': 'normal',
        'name': '퀴즈퀴즈',
        'id': 2,
        'description': "퀴즈를 해보세요.",
        'plus_description': "어디서 본 적이 있는 것 같은 건 기분 탓이에요",
        'required': None
    }
    me: AchievementContent = {
        'achievement_area': 'normal',
        'name': '-메-',
        'id': 3,
        'description': "자신만의 녜힁을 만들어보세요.",
        'plus_description': "읽으면 읽을 수록 힘이 빠진단 말이죠",
        'required': None
    }

    # Speak
    speak1: AchievementContent = {
        'achievement_area': 'speak',
        'name': '첫 인사',
        'id': 4,
        'description': "저와 대화를 나눠보세요. (대화의 기준은 서버에서만 사용 가능한 명령어들이에요!)",
        'plus_description': "기념비적인 첫 만남이에요",
        'required': 1
    }
    speak2: AchievementContent = {
        'achievement_area': 'speak',
        'name': '아직은 어색한 사이',
        'id': 5,
        'description': "50번 저와 대화를 나눠보세요.",
        'plus_description': "좀 익숙해졌나요?",
        'required': 50
    }
    speak3: AchievementContent = {
        'achievement_area': 'speak',
        'name': '이젠 친근함',
        'id': 6,
        'description': "250번 저와 대화를 나눠보세요.",
        'plus_description': "어쩐지 친근하고 좋은 걸요?",
        'required': 250
    }
    speak4: AchievementContent = {
        'achievement_area': 'speak',
        'name': '우리는 모두?',
        'id': 7,
        'description': "500번 저와 대화를 나눠보세요.",
        'plus_description': "친구!",
        'required': 500
    }
    speak5: AchievementContent = {
        'achievement_area': 'speak',
        'name': '알죠?',
        'id': 8,
        'description': "1,000번 저와 대화를 나눠보세요.",
        'plus_description': "이 정도면 다 알아요",
        'required': 1000
    }
    speak_h: AchievementContent = {
        'achievement_area': 'speak',
        'name': '이 정도면...',
        'id': 60,
        'description': "히든이에요!",
        'plus_description': "10000번 저와 대화를 나눠보세요. (중독이에요)",
        'required': 10000
    }

    # 출석 (ac)
    ac1: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍!',
        'id': 9,
        'description': "출석체크를 시도해보세요.",
        'plus_description': "뭔가가 많을 걸요",
        'required': 1
    }
    ac2: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X10',
        'id': 10,
        'description': "10번 출석체크를 시도해보세요.",
        'plus_description': "점점 익숙해져가요",
        'required': 10
    }
    ac3: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X50',
        'id': 11,
        'description': "50번 출석체크를 시도해보세요.",
        'plus_description': "서버는 마음에 드나요?",
        'required': 50
    }
    ac4: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X100',
        'id': 12,
        'description': "100번 출석체크를 시도해보세요.",
        'plus_description': "이젠 네임드겠군요",
        'required': 100
    }
    ac5: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X200',
        'id': 13,
        'description': "200번 출석체크를 시도해보세요.",
        'plus_description': "이렇게까지 꾸준할 수가!",
        'required': 200
    }
    ac6: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X365',
        'id': 14,
        'description': "365번 출석체크를 시도해보세요.",
        'plus_description': "축하해요! 자랑해도 좋아요",
        'required': 365
    }
    continuous_ac1: AchievementContent = {
        'achievement_area': 'ac',
        'name': '연속 출췍! X5',
        'id': 15,
        'description': "5번 연속으로 출석체크를 시도해보세요.",
        'plus_description': "꾸준함은 언제나 중요하기 마련이에요",
        'required': 5
    }
    continuous_ac2: AchievementContent = {
        'achievement_area': 'ac',
        'name': '연속 출췍! X10',
        'id': 16,
        'description': "10번 연속으로 출석체크를 시도해보세요.",
        'plus_description': "그리고 슬슬 귀찮아져요",
        'required': 10
    }
    continuous_ac3: AchievementContent = {
        'achievement_area': 'ac',
        'name': '연속 출췍! X50',
        'id': 17,
        'description': "50번 연속으로 출석체크를 시도해보세요.",
        'plus_description': "그냥보다 더 힘든 여정",
        'required': 50
    }
    continuous_ac4: AchievementContent = {
        'achievement_area': 'ac',
        'name': '연속 출췍! X100',
        'id': 18,
        'description': "100번 연속으로 출석체크를 시도해보세요.",
        'plus_description': "네임드 오브 네임드",
        'required': 100
    }
    continuous_ac5: AchievementContent = {
        'achievement_area': 'ac',
        'name': '연속 출췍! X365',
        'id': 19,
        'description': "365번 연속으로 출석체크를 시도해보세요.",
        'plus_description': "이건 좀 많이 대단한데요",
        'required': 365
    }
    ac_h: AchievementContent = {
        'achievement_area': 'ac',
        'name': '출췍! X∞',
        'id': 61,
        'description': "히든이에요!",
        'plus_description': "2년 동안 연속으로 출석체크를 시도하거나 3년 동안 출석체크를 시도해보세요. (그 만큼 서버가 재밌었다는 거겠죠! 한 잔 해~)",
        'required': {'continuous_ac_time': 1095, 'ac_time': 730}
    }
    
    wallet1: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '티끌 모아 태산',
        'id': 20,
        'description': "5,000원을 모으세요.",
        'plus_description': "첫 출발이에요",
        'required': 5000
    }
    wallet2: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '부자로 가는 한 걸음',
        'id': 21,
        'description': "50,000원을 모으세요.",
        'plus_description': "어느새 이 정도라니!",
        'required': 50000
    }
    wallet3: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '꽤 많은데?',
        'id': 22,
        'description': "100,000원을 모으세요.",
        'plus_description': "10만이면 많은 게 맞죠",
        'required': 100000
    }
    wallet4: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '꽤 많은 걸 넘어',
        'id': 23,
        'description': "500,000원을 모으세요.",
        'plus_description': "100만이 코?앞이에요",
        'required': 500000
    }
    wallet5: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '백만 장자',
        'id': 24,
        'description': "1,000,000원을 모으세요.",
        'plus_description': "반짝반짝해!",
        'required': 1000000
    }
    wallet6: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '천만 장자',
        'id': 25,
        'description': "10,000,000원을 모으세요.",
        'plus_description': "천만 돌파!",
        'required': 10000000
    }
    wallet7: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '일억 장자',
        'id': 26,
        'description': "100,000,000원을 모으세요.",
        'plus_description': "이젠 한계에요",
        'required': 100000000
    }
    wallet_h1: AchievementContent = {
        'achievement_area': 'wallet',
        'name': '제 재산력은...',
        'id': 62,
        'description': "히든이에요!",
        'plus_description': "정확하게 530,000원을 모으세요. (\"나 화났다! `{userName}`!\")",
        'required': 530000
    }
    wallet_h2: AchievementContent = {
        'achievement_area': 'wallet',
        'name': ':(',
        'id': 63,
        'description': "히든이에요!",
        'plus_description': "1,000,000,000,000원을 모으세요. (과학적 표기법을 고려해야 되겠어요)",
        'required': 1000000000000
    }
    
    # Gamble
    gamble_play1: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박 입문',
        'id': 27,
        'description': "처음 도박을 해보세요.",
        'plus_description': "하지만 빠져들지는 마세요",
        'required': 1
    }
    gamble_play2: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박 초보',
        'id': 28,
        'description': "10번 도박을 해보세요.",
        'plus_description': "좀 돈은 땄나요",
        'required': 10
    }
    gamble_play3: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박 중수',
        'id': 29,
        'description': "50번 도박을 해보세요.",
        'plus_description': "잃을 때도 많겠죠",
        'required': 50
    }
    gamble_play4: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박 고수',
        'id': 30,
        'description': "100번 도박을 해보세요.",
        'plus_description': "그래도 힘내요",
        'required': 100
    }
    gamble_play5: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박 초고수',
        'id': 31,
        'description': "250번 도박을 해보세요.",
        'plus_description': "언제나 도박 상담은 1336이 있으니까 말이죠",
        'required': 250
    }
    gamble_earn1: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '오예',
        'id': 32,
        'description': "돈을 따보세요.",
        'plus_description': "어때요?",
        'required': None
    }
    gamble_earn2: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '이 정도는 적나',
        'id': 33,
        'description': "누적 5,000원을 따보세요.",
        'plus_description': "5,000원은 너무 적지 않나요",
        'required': 5000
    }
    gamble_earn3: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '짤랑짤랑',
        'id': 34,
        'description': "누적 25,000원을 따보세요.",
        'plus_description': "오",
        'required': 25000
    }
    gamble_earn4: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '많다 많아',
        'id': 35,
        'description': "누적 125,000원을 따보세요.",
        'plus_description': "다음은 몇원을 따야 하는지 알겠죠?",
        'required': 125000
    }
    gamble_earn5: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '도박의 귀재',
        'id': 36,
        'description': "누적 625,000원을 따보세요.",
        'plus_description': "진짜로 많기도 하군요",
        'required': 625000
    }
    gamble_lose1: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '?',
        'id': 37,
        'description': "돈을 잃으세요.",
        'plus_description': "운이 안 좋았어요",
        'required': None
    }
    gamble_lose2: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '???',
        'id': 38,
        'description': "누적 5,000원을 잃으세요.",
        'plus_description': "5,000원도 너무 많아요",
        'required': 5000
    }
    gamble_lose3: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '지갑에 구멍이 났나',
        'id': 39,
        'description': "누적 25,000원을 잃으세요.",
        'plus_description': "이런",
        'required': 25000
    }
    gamble_lose4: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '계속된 잃음',
        'id': 40,
        'description': "누적 125,000원을 잃으세요.",
        'plus_description': "힘내요",
        'required': 125000
    }
    gamble_lose5: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '미련 버려요',
        'id': 41,
        'description': "누적 625,000원을 잃으세요.",
        'plus_description': "다음부턴 새 인생 사시길 바랍니다",
        'required': 625000
    }
    gamble_h1: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '이건 그냥 도박 중독증',
        'id': 64,
        'description': "히든이에요!",
        'plus_description': "1,000번 도박을 해보세요. (결과는 어땠나요)",
        'required': 1000
    }
    gamble_h2: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '치료가 필요할 정도로 심각한 \'도박 중독증\'입니다.',
        'id': 65,
        'description': "히든이에요!",
        'plus_description': "정확하게 10,000,000원을 배팅하세요. (\"흥, 웃기는 소리.\")",
        'required': 10000000
    }
    gamble_h3: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '딱 본전만 챙기고 간다',
        'id': 66,
        'description': "히든이에요!",
        'plus_description': "모든 재산을 전부 배팅한 뒤, 다시 돌려 받으세요. (말 그대로 본전만 뽑았네요)",
        'required': None
    }
    gamble_h4: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '전설의 도박꾼',
        'id': 67,
        'description': "히든이에요!",
        'plus_description': "누적 100,000,000원을 따보세요. (운이 좋네요)",
        'required': 100000000
    }
    gamble_h5: AchievementContent = {
        'achievement_area': 'gamble',
        'name': '티끌을 모아도',
        'id': 68,
        'description': "히든이에요!",
        'plus_description': "도박으로 한 번에 모든 돈을 잃으세요. (\"돈은 거들 뿐\")",
        'required': 0
    }
    
    # Fight
    fight1: AchievementContent = {
        'achievement_area': 'fight',
        'name': '전투의 세계',
        'id': 42,
        'description': "누군가랑 싸우세요.",
        'plus_description': "불화는 없었으면 좋겠네요",
        'required': 1
    }
    fight2: AchievementContent = {
        'achievement_area': 'fight',
        'name': '좀 싸워본',
        'id': 43,
        'description': "누군가랑 5번 싸우세요.",
        'plus_description': "싸우는 걸 즐기는 건 아니겠죠",
        'required': 5
    }
    fight3: AchievementContent = {
        'achievement_area': 'fight',
        'name': '난 아직 피를 원한다',
        'id': 44,
        'description': "누군가랑 25번 싸우세요.",
        'plus_description': "사실 재밌긴 해요",
        'required': 25
    }
    fight4: AchievementContent = {
        'achievement_area': 'fight',
        'name': '멈춰!',
        'id': 45,
        'description': "누군가랑 125번 싸우세요.",
        'plus_description': "폭력적이야!",
        'required': 125
    }
    fight_h1: AchievementContent = {
        'achievement_area': 'fight',
        'name': '사이어인?',
        'id': 69,
        'description': "히든이에요!",
        'plus_description': "누군가랑 625번 싸우세요. (\"감히 인간 주제에 사이어인의 힘을 평가하지 말라.\")",
        'required': 625
    }
    fight_h2: AchievementContent = {
        'achievement_area': 'fight',
        'name': '전투 조류',
        'id': 70,
        'description': "히든이에요!",
        'plus_description': "빈사 상태로 상대를 이기세요. (\"이것도 계산한 거냐! 죠죠!!!\")",
        'required': None
    }

    
    # Tropy
    tropy1: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 I',
        'id': 50,
        'description': "5개의 업적을 달성하세요!",
        'plus_description': "여기까지는 쉽죠?",
        'required': 5
    }
    tropy2: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 II',
        'id': 51,
        'description': "10개의 업적을 달성하세요!",
        'plus_description': "여기까지도 쉬울 거에요",
        'required': 10
    }
    tropy3: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 III',
        'id': 52,
        'description': "15개의 업적을 달성하세요!",
        'plus_description': "이제 어렵겠네요",
        'required': 15
    }
    tropy4: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 IV',
        'id': 53,
        'description': "20개의 업적을 달성하세요!",
        'plus_description': "거의 절반이에요",
        'required': 20
    }
    tropy5: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 V',
        'id': 54,
        'description': "25개의 업적을 달성하세요!",
        'plus_description': "절반도 거의 넘었군요",
        'required': 25
    }
    tropy6: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 VI',
        'id': 55,
        'description': "30개의 업적을 달성하세요!",
        'plus_description': "그리고 30",
        'required': 30
    }
    tropy7: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 VII',
        'id': 56,
        'description': "35개의 업적을 달성하세요!",
        'plus_description': "다 왔어요",
        'required': 35
    }
    tropy8: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 VIII',
        'id': 57,
        'description': "40개의 업적을 달성하세요!",
        'plus_description': "사실 더 남았어요",
        'required': 40
    }
    tropy9: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 콜렉터 IX',
        'id': 58,
        'description': "45개의 업적을 달성하세요!",
        'plus_description': "진짜로 다 왔어요",
        'required': 45
    }
    tropy_all: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '업적 올 콜렉터',
        'id': 59,
        'description': "모든 업적을 달성하세요!",
        'plus_description': "수고했어요",
        'required': None
    }
    tropy_hidden1: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '히든 콜렉터 I',
        'id': 46,
        'description': "3개의 히든 업적을 달성하세요!",
        'plus_description': "고생하세요",
        'required': 3
    }
    tropy_hidden2: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '히든 콜렉터 II',
        'id': 47,
        'description': "6개의 히든 업적을 달성하세요!",
        'plus_description': "절반도 안 남았군요",
        'required': 6
    }
    tropy_hidden3: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '히든 콜렉터 III',
        'id': 48,
        'description': "9개의 히든 업적을 달성하세요!",
        'plus_description': "하나만 더!",
        'required': 9
    }
    tropy_hidden_all: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '히든 올 콜렉터',
        'id': 49,
        'description': "모든 히든 업적을 달성하세요!",
        'plus_description': "고생했어요",
        'required': None
    }
    tropy_real_all: AchievementContent = {
        'achievement_area': 'tropy',
        'name': '진정한 업적 올 콜렉터',
        'id': 71,
        'description': "히든을 포함한 모든 업적을 달성하세요!",
        'plus_description': "그리고 이게 정녕 의미 있는 행동이었는지 되돌아보세요.",
        'required': None
    }

def getAchievementData() -> Dict[str, AchievementContent]:
    result:Dict[str, dict] = {
        key: value
        for key, value in Achievement.__dict__.items()
        if isinstance(value, dict) and not key.startswith('__')
    }
    castedResult:Dict[str, AchievementContent] = cast(Dict[str, AchievementContent], result)
    return castedResult

def getDefaultAchievementData() -> Dict[str, Literal[False]]:
    return {
        key: False
        for key, value in getAchievementData().items()
    }