from library.SaveData import *
from library.utils.PVPUtil import PVPUtil
from enum import Enum
from library.Achievement import getDefaultAchievementData

class DefaultServerEnum(Enum):
    NORMAL = {
        'balance': 0,
        'xp': 0,
        'level': 0
    }
    SYSTEM = {
        'server_introduction': {
            'title': None,
            'content': None,
            'show_other_server': False
        },
        'server_role': {
            'title': None,
            'content': None
        }
    }

class DefaultUserEnum(Enum):
    NORMAL = {
        'balance': 0,
        'xp': 0,
        'level': 0,
        'date': [
            0,
            0
        ],
        'ac_time': 0,
        'continuous_ac_time': 1,
        'db_count': 0
    }
    INTRODUCTION = {
        'title': None,
        'content': None
    }
    GAMBLE = {
        'wins': 0,
        'loses': 0,
        'ties': 0,
        'gamble_cooldown': 0,
        'already_gamble': False
    }
    PVP = {
        'stats': {
            'point': 10,
            'str': 0, # 힘 등등
            'int': 0, # 지능 등등
            'dex': 0, # 민첩 등등 (원래 번역은 재주가 맞다고 함)
            'def': 0, # 방어 등등
            'con': 0, # 체력 등등 # 0은 안 찍음, 그 외에는 스킬 레벨
        },
        'skilltree': { 
            'point': 1,
            'skill': PVPUtil.getDefaultSkillTreeData()
        }
    }
    ACHIEVEMENT = getDefaultAchievementData()

class SaveDataUtil():
    @staticmethod
    def isServerInData(data:SaveData, serverID:str) -> bool:
        return serverID in data

    @staticmethod
    def isUserInData(data:SaveData, userID:str, serverID:Optional[str] = None) -> bool:
        return f'{serverID}/{userID}' in data or userID in data

    @classmethod
    def initServer(cls, data:SaveData, serverID:str, initType:Optional[DefaultServerEnum] = None) -> None:
        if data.dataType.isServerScoped and initType == None: 
#            path:str = os.path.join(data.FILE_PATH, serverID)
#            os.makedirs(path, exist_ok=True)
            return
        if cls.isServerInData(data, serverID) and initType != None :
            cls.deepUpdateData(data, initType.value, serverID)
            return
        data.set(cast(DefaultServerEnum, initType).value, serverID)

    @classmethod
    def initUser(cls, data:SaveData, userID:str, initType:DefaultUserEnum, serverID:Optional[str] = None) -> None:
        if cls.isUserInData(data, userID, serverID):
            cls.deepUpdateData(data, initType.value, serverID, userID)
            return
        if serverID and not cls.isServerInData(data, str(serverID)):
            cls.initServer(data, str(serverID))
        
        data.set(initType.value, serverID, userID)
        
    @classmethod
    def deepMergeDict(cls, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if key not in target:
                target[key] = value
                continue
                
            if isinstance(target[key], dict) and isinstance(value, dict):
                cls.deepMergeDict(target[key], value)
        
    @classmethod
    def deepUpdateData(cls, data:SaveData, updates:dict, serverID:Optional[str] = None, userID:Optional[str] = None):
        currentData:dict = data.get(serverID=serverID, userID=userID)
        if not isinstance(currentData, dict):
            currentData = {}

        cls.deepMergeDict(currentData, updates)

        data.set(currentData, serverID, userID)
