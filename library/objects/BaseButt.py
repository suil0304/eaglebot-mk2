from discord import Interaction, ButtonStyle
from discord.ui import View
from discord.errors import NotFound
from typing import Callable, Coroutine, Any, TypedDict, Dict, List
from functools import reduce
from operator import getitem

BUTT_CALLBACK_TYPE = Callable[[Interaction], Coroutine[Any, Any, None]]
TIMEOUT_CALLBACK_TYPE = Callable[[Interaction], Coroutine[Any, Any, None]]

async def nothingCallback(interaction:Interaction | None):
    pass

async def defaultTimeoutCallback(ctx:Interaction):
    await ctx.edit_original_response(content="버튼은 쌓이면 머리가 아픈 거에요!", embed=None, view=None)

class BaseButtContent(TypedDict):
    label:str
    row:int
    style:ButtonStyle
    disable:bool
    
DISABLE_BUTT:BaseButtContent = {'label': 'ㅤ', 'row': 0, 'style': ButtonStyle.primary, 'disable': True}

class BaseButt(View):
    variables:Dict[str, Any] = {}

    def __init__(
        self,
        originalInteraction:Interaction,
        timeout:float = 180,
        /,
    ):
        super().__init__(timeout=timeout)
        
        self.originalInteraction:Interaction = originalInteraction
        self.timeoutCallback:TIMEOUT_CALLBACK_TYPE = defaultTimeoutCallback
        
        # like FNF Psych Engine's Lua (Map<String, Dynamic>)
        self.variables:Dict[str, Any] = {}
        
    async def on_timeout(self):
        try:
            self.variables = {}
            await self.timeoutCallback(self.originalInteraction)
            
        except NotFound:
            return
        
        except Exception as error:
            print(error)
            
            return
        
    def initProperty(self, tag:str, value:Any) -> None:
        keys:List[str] = tag.split('.')
        
        target:Dict[str, Any] = {}
        try:
            target = reduce(getitem, keys[:-1], self.variables)
            
        except (KeyError, TypeError):
            raise ValueError(f'`{tag}`로는 접근할 수 없음')
        
        if target.get(keys[-1]) != None:
            return
        
        target[keys[-1]] = value
        
    def getProperty(self, tag: str) -> Any:
        keys:List[str] = tag.split('.')
        
        try:
            return reduce(getitem, keys, self.variables)
        
        except (KeyError, TypeError):
            return None
    
    def setProperty(self, tag: str, value: Any) -> None:
        keys:List[str] = tag.split('.')
        
        try:
            target:Dict[str, Any] = reduce(getitem, keys[:-1], self.variables)
            target[keys[-1]] = value
            
        except (KeyError, TypeError):
            raise ValueError(f'`{tag}`로는 접근할 수 없음')