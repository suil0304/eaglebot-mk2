

class GambleUtil():
    @staticmethod
    def calcWinningRate(winNum:int, loseNum:int, tieNum:int) -> int | float:
        result:float = (winNum / max(1, winNum + loseNum + tieNum)) * 100
        
        if result.is_integer():
            return int(result)
        else:
            return round(result, 2)
        
    @staticmethod
    def calcAllPlayCount(winNum:int, loseNum:int, tieNum:int) -> int:
        return winNum + loseNum + tieNum