from typing import Any
from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def from_any(cls, value:Any) -> 'BaseEnum':
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f'{value}는 유효한 {cls.__name__} 값이 아님')

    @classmethod
    def getItemLength(cls) -> int:
        return len(list(cls))