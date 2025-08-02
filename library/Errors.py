from discord import Embed
from typing import TypedDict, NoReturn
from library.utils.NormalUtil import NormalUtil
from datetime import datetime

class SmallError(Exception): pass
class BigError(Exception): pass

class ErrorEmbedContent(TypedDict):
    id:int
    name:str
    description:str
    error:type[Exception]

class ErrorEmbedType():
    CALLED_FROM_NOT_GUILD:ErrorEmbedContent = {
        'id': 1,
        'name': 'Called from not guild',
        'description': 'You called this command from not guild location.\nPlease use this command in guild.',
        'error': SmallError
    }
    NOT_A_USER:ErrorEmbedContent = {
        'id': 2,
        'name': 'Not a user',
        'description': 'Using data from not user.',
        'error': BigError
    }
    BOT_LOGOUTED:ErrorEmbedContent = {
        'id': 3,
        'name': 'Bot logouted',
        'description': 'Already bot is logouted.',
        'error': BigError
    }
    
class ErrorUtil():
    @staticmethod
    def runError(errorType:ErrorEmbedContent, now:datetime) -> NoReturn:
        raise errorType['error'](f'Error no.{errorType["id"]}: {errorType["name"]}\n{errorType["description"]}\nby {now}')
    
    @staticmethod
    def getErrorEmbed(errorType:ErrorEmbedContent, now:datetime) -> Embed:
        embed:Embed = Embed(
            title=f'Error no.{errorType["id"]}: {errorType["name"]}',
            description=errorType['description'],
            color=NormalUtil.EAGLE_COLOR,
            timestamp=now
        )
        return embed