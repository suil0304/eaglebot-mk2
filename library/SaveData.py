"""
give me save, mama!
"""

import json
import os
import shutil
import typing
import firebase_admin
from firebase_admin import credentials, db
from library.BaseEnum import BaseEnum
from typing import Any, Dict, Union, cast, Optional, List

class SaveDataTypeEnum(BaseEnum):
    SERVER_NORMAL = 'server_data'
    SERVER_SYSTEM = 'server_data_system'
    NORMAL = 'user_data'
    USER_INTRODUCTION = 'user_introduction'
    GAMBLE = 'user_data_gamble'
    RPG = 'user_data_rpg'
    ACHIEVEMENT = 'user_data_achievement'
    
    @property
    def isServerScoped(self) -> bool:
        if self.name.startswith('USER'):
            return False
        elif self.name.startswith('SERVER'):
            return False
        return True

# class SaveData:
#     dataType:SaveDataTypeEnum
#     FILE_PATH:str
    
#     def __init__(self, dataType:Union[str, SaveDataTypeEnum]):
#         if isinstance(dataType, str):
#             _dataType:SaveDataTypeEnum = cast(SaveDataTypeEnum, SaveDataTypeEnum.from_any(dataType))
#         else:
#             _dataType:SaveDataTypeEnum = dataType
#         self.dataType = _dataType
#         self.FILE_PATH = os.path.join('database', _dataType.value)

#     def _getFilePath(self, serverID:Optional[str] = None, userID:Optional[str] = None) -> str:
#         if self.dataType.isServerScoped:
#             if not serverID:
#                 raise ValueError(f"[SaveData] '{self.dataType.name}' 타입은 serverID가 필요함!")
#             if not userID:
#                 raise ValueError(f"[SaveData] '{self.dataType.name}' 타입은 userID가 필요함!")
#             return os.path.join(self.FILE_PATH, serverID, f'{userID}.json')
#         else:
#             if not userID:
#                 if not serverID:
#                     raise ValueError(f"[SaveData] 아무 것도 주어지지 않음!")
#                 return os.path.join(self.FILE_PATH, f'{serverID}.json')
#             return os.path.join(self.FILE_PATH, f'{userID}.json')

#     def get(self, *, serverID:Optional[str] = None, userID:Optional[str] = None, data:Optional[str] = None, default:Any = None) -> Any | Dict[str, Any]:
#         path:str = self._getFilePath(serverID, userID)
#         try:
#             with open(path, 'r') as f:
#                 fileData:Dict[str, Any] = json.load(f)
#                 return fileData.get(data, default) if data else fileData
#         except FileNotFoundError:
#             print(f'[SaveData] {path} 파일 없음')
#             return default if data else {}

#     def set(self, data:dict, serverID:Optional[str] = None, userID:Optional[str] = None) -> None:
#         path:str = self._getFilePath(serverID, userID)
#         os.makedirs(os.path.dirname(path), exist_ok=True)
#         with open(path, 'w') as f:
#             json.dump(data, f, indent=4)

#     def update(self, updates:dict, serverID:Optional[str] = None, userID:Optional[str] = None) -> None:
#         currentData:Dict[str, Any] = self.get(serverID=serverID, userID=userID)
#         if not isinstance(currentData, dict):
#             currentData = {}
#         currentData.update(updates)
#         self.set(currentData, serverID, userID)

#     def remove(self, *, serverID:Optional[str] = None, userID:Optional[str] = None, deleteServer:bool = False) -> None:
#         if self.dataType.isServerScoped:
#             if deleteServer and serverID:
#                 serverPath:str = os.path.join(self.FILE_PATH, serverID)
#                 if os.path.exists(serverPath):
#                     shutil.rmtree(serverPath)
#                     print(f'[SaveData] 서버 {serverID} 전체 데이터 삭제됨')
#             else:
#                 if not serverID or not userID:
#                     raise ValueError('[SaveData] 서버 범위 삭제 시 serverID, userID 둘 다 필요함')
#                 path:str = self._getFilePath(serverID, userID)
#                 if os.path.exists(path):
#                     os.remove(path)
#                     print(f'[SaveData] 서버 {serverID}의 유저 {userID} 데이터 삭제됨')
#         else:
#             if deleteServer:
#                 raise ValueError(f"[SaveData] 글로벌 스코프 데이터는 deleteServer 불가능")
#             if not userID:
#                 raise ValueError('[SaveData] 글로벌 유저 데이터 삭제 시 userID 필요함')
#             path:str = self._getFilePath(userID=userID)
#             if os.path.exists(path):
#                 os.remove(path)
#                 print(f'[SaveData] 글로벌 유저 {userID} 데이터 삭제됨')

#     def getUsers(self, serverID:str) -> Dict[str, Dict[str, Any]]:
#         if not self.dataType.isServerScoped:
#             raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
#         targetPath:str = os.path.join(self.FILE_PATH, serverID)
#         try:
#             result:Dict[str, Dict[str, Any]] = {}
#             for userFile in os.listdir(targetPath):
#                 fullPath:str = os.path.join(targetPath, userFile)
#                 if os.path.isfile(fullPath) and userFile.endswith('.json'):
#                     with open(fullPath, 'r') as f:
#                         userID:str = userFile[:-5]
#                         result[userID] = json.load(f)
#             return result
#         except FileNotFoundError:
#             return {}

#     def getServerLength(self) -> int:
#         if not self.dataType.isServerScoped:
#             raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
#         try:
#             return len([
#                 name for name in os.listdir(self.FILE_PATH)
#                 if os.path.isdir(os.path.join(self.FILE_PATH, name))
#             ])
#         except FileNotFoundError:
#             return 0

#     def getUserLength(self, serverID:str) -> int:
#         if not self.dataType.isServerScoped:
#             raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
#         targetPath:str = os.path.join(self.FILE_PATH, serverID)
#         try:
#             return len([
#                 name for name in os.listdir(targetPath)
#                 if os.path.isfile(os.path.join(targetPath, name)) and name.endswith('.json')
#             ])
#         except FileNotFoundError:
#             return 0

#     def __contains__(self, key:str) -> bool:
#         parts:List[str] = key.split('/')
#         if self.dataType.isServerScoped:
#             if len(parts) != 2:
#                 return False
#             targetPath:str = self._getFilePath(parts[0], parts[1])
#         else:
#             if len(parts) != 1:
#                 return False
#             targetPath:str = self._getFilePath(userID=parts[0])
#         return os.path.exists(targetPath)


def initialize_firebase():
    if not firebase_admin._apps:
        raw_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if not raw_json:
            raise RuntimeError("FIREBASE_CREDENTIALS_JSON 환경변수가 비어 있음!")

        cred_dict = json.loads(raw_json)
        cred = credentials.Certificate(cred_dict)

        db_url = os.getenv("FIREBASE_DATABASE_URL")
        if not db_url:
            raise RuntimeError("FIREBASE_DATABASE_URL 환경변수가 비어 있음!")

        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })

initialize_firebase()

class SaveData:
    def __init__(self, dataType:Union[str, SaveDataTypeEnum]):
        if isinstance(dataType, str):
            _dataType = cast(SaveDataTypeEnum, SaveDataTypeEnum[dataType.upper()])
        else:
            _dataType = dataType
        self.dataType = _dataType

    def _get_db_ref(self, serverID:Optional[str] = None, userID:Optional[str] = None):
        base_ref = db.reference(self.dataType.value)
        if self.dataType.isServerScoped:
            if not serverID:
                raise ValueError(f"[SaveData] '{self.dataType.name}' 타입은 serverID가 필요함!")
            if not userID:
                raise ValueError(f"[SaveData] '{self.dataType.name}' 타입은 userID가 필요함!")
            return base_ref.child(serverID).child(userID)
        else:
            if userID:
                return base_ref.child(userID)
            elif serverID:
                return base_ref.child(serverID)
            else:
                return base_ref

    def get(self, *, serverID:Optional[str] = None, userID:Optional[str] = None, data:Optional[str] = None, default:Any = None) -> Any:
        ref = self._get_db_ref(serverID, userID)
        snapshot = ref.get()
        if snapshot is None:
            return default if data else {}
        if data:
            return snapshot.get(data, default) if isinstance(snapshot, dict) else default
        return snapshot

    def set(self, data:dict, serverID:Optional[str] = None, userID:Optional[str] = None) -> None:
        ref = self._get_db_ref(serverID, userID)
        ref.set(data)

    def update(self, updates:dict, serverID:Optional[str] = None, userID:Optional[str] = None) -> None:
        ref = self._get_db_ref(serverID, userID)
        ref.update(updates)

    def remove(self, *, serverID:Optional[str] = None, userID:Optional[str] = None, deleteServer:bool = False) -> None:
        base_ref = db.reference(self.dataType.value)
        if self.dataType.isServerScoped:
            if deleteServer and serverID:
                base_ref.child(serverID).delete()
                print(f'[SaveData] 서버 {serverID} 전체 데이터 삭제됨')
            else:
                if not serverID or not userID:
                    raise ValueError('[SaveData] 서버 범위 삭제 시 serverID, userID 둘 다 필요함')
                base_ref.child(serverID).child(userID).delete()
                print(f'[SaveData] 서버 {serverID}의 유저 {userID} 데이터 삭제됨')
        else:
            if deleteServer:
                raise ValueError("[SaveData] 글로벌 스코프 데이터는 deleteServer 불가능")
            if not userID:
                raise ValueError('[SaveData] 글로벌 유저 데이터 삭제 시 userID 필요함')
            base_ref.child(userID).delete()
            print(f'[SaveData] 글로벌 유저 {userID} 데이터 삭제됨')

    def getUsers(self, serverID:str) -> Dict[str, Dict[str, Any]]:
        if not self.dataType.isServerScoped:
            raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
        base_ref = db.reference(self.dataType.value)
        server_ref = base_ref.child(serverID)
        snapshot = server_ref.get()
        if not snapshot:
            return {}
        return snapshot

    def getServerLength(self) -> int:
        if not self.dataType.isServerScoped:
            raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
        base_ref = db.reference(self.dataType.value)
        snapshot = base_ref.get()
        if not snapshot:
            return 0
        return len(snapshot.keys())

    def getUserLength(self, serverID:str) -> int:
        if not self.dataType.isServerScoped:
            raise ValueError(f'[SaveData] {self.dataType.name}는 서버 단위 데이터가 아님')
        base_ref = db.reference(self.dataType.value)
        server_ref = base_ref.child(serverID)
        snapshot = server_ref.get()
        if not snapshot:
            return 0
        return len(snapshot.keys())

    def __contains__(self, key:str) -> bool:
        parts = key.split('/')
        if self.dataType.isServerScoped:
            if len(parts) != 2:
                return False
            ref = self._get_db_ref(parts[0], parts[1])
        else:
            if len(parts) != 1:
                return False
            ref = self._get_db_ref(userID=parts[0])
        snapshot = ref.get()
        return snapshot is not None
        
# server
dataServer:SaveData = SaveData(SaveDataTypeEnum.SERVER_NORMAL)
dataServerSystem:SaveData = SaveData(SaveDataTypeEnum.SERVER_SYSTEM)
datasServer:typing.List[SaveData] = [
    dataServer,
    dataServerSystem
]
# user
dataUser:SaveData = SaveData(SaveDataTypeEnum.NORMAL)
dataUserIntroduction:SaveData = SaveData(SaveDataTypeEnum.USER_INTRODUCTION)
dataUserGamble:SaveData = SaveData(SaveDataTypeEnum.GAMBLE)
dataUserRPG:SaveData = SaveData(SaveDataTypeEnum.RPG)
dataUserAchievement:SaveData = SaveData(SaveDataTypeEnum.ACHIEVEMENT)
datasUser:typing.List[SaveData] = [
    dataUser,
    dataUserIntroduction,
    dataUserGamble,
    dataUserRPG,
    dataUserAchievement
]

datasAll:typing.List[SaveData] = datasUser.copy() + datasServer.copy()