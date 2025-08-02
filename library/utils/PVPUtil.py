from library.preimport import *

SKILL_AREA = Literal[
    'attack',
    'defense',
    'util',
]

class PVPState(Enum):
    ERROR = -1
    NORMAL = 0
    ATTACK = 1
    DEFENSE = 1
    DODGE = 2
    
class SkillTreeContent(TypedDict):
    skill_area:SKILL_AREA
    name:str
    description:str
    num_of_skill:int
    max_level:int
    level_lock:List[int]
    point_lock:List[int]
    
class SkillTree():
    # attack
    better_attack:SkillTreeContent = {
        'skill_area': 'attack',
        'name': '더 나은 공격',
        'description': '이 스킬을 찍으면 공격 계산 수식이 더 나아집니다.',
        'num_of_skill': 5,
        'max_level': 3,
        'level_lock': [0, 6, 13, 20, 27],
        'point_lock': [0, 2, 6, 11, 18]
    }
    
    # defense
    better_defense:SkillTreeContent = {
        'skill_area': 'defense',
        'name': '더 나은 방어',
        'description': '이 스킬을 찍으면 방어 계산 수식이 더 나아집니다.',
        'num_of_skill': 5,
        'max_level': 3,
        'level_lock': [0, 3, 7, 14, 22],
        'point_lock': [0, 2, 3, 6, 9]
    }
    
    # util
    better_luck:SkillTreeContent = {
        'skill_area': 'util',
        'name': '더 나은 운',
        'description': '이 스킬을 찍으면 운이 더 나아집니다.',
        'num_of_skill': 3,
        'max_level': 1,
        'level_lock': [4, 16, 36],
        'point_lock': [3, 8, 18]
    }
    
class PVPUtil():
    @staticmethod
    def getDefaultSkillTreeData() -> dict[str, list[int]]:
        return {
            key: [0] * value['num_of_skill']
            for key, value in SkillTree.__dict__.items()
            if isinstance(value, dict) and 'num_of_skill' in value and not key.startswith('__')
        }