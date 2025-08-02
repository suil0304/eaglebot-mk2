from library.preimport import *
from numpy import log2

BASE_TYPE = Literal['user', 'server']

class LevelUtil():
    XP_CLAIM_INTERVAL:int = 86400

    XP_BASE:int = 50
    XP_BASE_TOTAL:int = 100
    XP_BASE_TOTAL_SERVER:int = XP_BASE_TOTAL * 10
    XP_INCREASE_MULT:float = 1.15
    
    XP_BAR_LEFT_EMPTY:str = '<:leftbin_xpbar:1335620860224082092>'
    XP_BAR_MIDDLE_EMPTY:str = '<:middlebin_xpbar:1335620891006210089>'
    XP_BAR_RIGHT_EMPTY:str = '<:rightbin_xpbar:1335620919057580084>'
    XP_BAR_LEFT_FULL:str = '<:leftfull_xpbar:1335620872232239124>'
    XP_BAR_MIDDLE_FULL:str = '<:middlefull_xpbar:1335620901546233867>'
    XP_BAR_RIGHT_FULL:str = '<:rightfull_xpbar:1335620927899304016>'
    
    @classmethod
    def makeXPBar(cls) -> List[str]:
        def buildBar(progress_index: int) -> str:
            left:str = cls.XP_BAR_LEFT_FULL if progress_index > 0 else cls.XP_BAR_LEFT_EMPTY
            middles:str = ''
            
            for i in range(9):
                if i < progress_index:
                    middles += cls.XP_BAR_MIDDLE_FULL
                else:
                    middles += cls.XP_BAR_MIDDLE_EMPTY
                    
            right:str = cls.XP_BAR_RIGHT_FULL if progress_index == 11 else cls.XP_BAR_RIGHT_EMPTY
            
            return left + middles + right
        
        return [buildBar(i) for i in range(11)] + [buildBar(11)]
    
    @classmethod
    def makeThresholds(cls, level:int, base:BASE_TYPE = 'user') -> List[float]:
        baseXP:int = cls.calcLevelXPTotal(level, base)
        
        return [baseXP * (i / 10) for i in range(11)]
    
    @classmethod
    def calcXP(cls, continuousAC:int) -> int:
        if continuousAC < 0:
            raise ValueError()
        
        return int(cls.XP_BASE + log2(continuousAC))

    @classmethod
    def calcLevelXPTotal(cls, level:int, base:BASE_TYPE = 'user') -> int:
        if level < 0:
            raise ValueError()
    
        _base:int = cls.XP_BASE_TOTAL if base == 'user' else cls.XP_BASE_TOTAL_SERVER
        loggedTotal:int = int(_base * log2(level + 1) * cls.XP_INCREASE_MULT)
        
        return max(_base, loggedTotal)
    
    @classmethod
    def isLevelIncrease(cls, xp:int, total:int) -> bool:
        return xp >= total