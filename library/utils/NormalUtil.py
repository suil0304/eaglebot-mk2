from discord import Color, Guild, ClientUser, User, app_commands, Interaction
from typing import Callable, Any, TypeGuard, Dict, Union, Coroutine
from datetime import datetime

class NormalUtil():
    BOOTING_TIME:datetime = datetime.now()
    EAGLE_COLOR:Color = Color.from_rgb(139, 69, 19)
    
    @classmethod
    def forEach(cls, objs:list, func:Callable[[Any], None]) -> None:
        """
        huh, this is stealing function of FlxGroup.
        but pretty good.

        Parameters:
            objs (list): put your list
            func (Callable[[Any], None]): and using your func
        """
        for obj in objs:
            if obj is not None:
                if isinstance(obj, list):
                    cls.forEach(obj, func)
                else:
                    func(obj)
                    
    @staticmethod
    def isInteractionServer(guild:Guild | None) -> TypeGuard[Guild]:
        """
        is this Interaction from server?

        Args:
            guild (Guild | None): your guild

        Returns:
            TypeGuard[Guild]: safe guard of guild
        """
        return guild != None
        
    @staticmethod
    def isUser(user:ClientUser | User | None) -> TypeGuard[ClientUser | User]:
        """
        is this user valid user?

        Args:
            user (ClientUser | User | None): your user

        Returns:
            TypeGuard[ClientUser]: safe guard of user
        """
        return user != None
                    
    @staticmethod
    def objNullChecks(log:bool = True, /, **kwargs:Any) -> bool:
        """
        object null checker

        Args:
            log (bool): trace log?
            kwargs (Any): put this key

        Returns:
            bool: if object is null, return False, else, return True
        """
        objNullDict:Dict[str, None] = {}
        
        for key, value in kwargs.items():
            if value is None:
                objNullDict[key] = None
                
        isObjNull:bool = None in objNullDict.values()
        if log and isObjNull:
            print(f"{list(objNullDict.keys())} 값이 None임")
            
        return False if isObjNull else True
                    
    @staticmethod
    def convertSecondsToTime(seconds: int) -> tuple[int, int, int]:
        """
        seconds to time coverter.
        
        Parameters:
            seconds (int): seconds
            
        Returns:
            hour, minute, second
        """
        second:int = seconds % 60
        minute:int = (seconds // 60) % 60
        hour:int = seconds // 60 // 60
        
        return int(hour), int(minute), int(second)