import discord
from typing import Literal, Dict, cast
from library.SaveData import *
from library.utils.SaveDataUtil import *
from library.Achievement import *

class AchievementUtil():
    @staticmethod
    async def achievementUnlockMessage(ctx:discord.Interaction, bigAchievementName:str, smallAchievementName:str, isHidden:bool = False):
        await ctx.followup.send(
            f"✅ `{bigAchievementName}`의 {'**히든 업적**, ' if isHidden else ''}`{smallAchievementName}`을 달성했어요!\n"
            "`/업적`으로 확인해보세요!",
            ephemeral=True
        )
    
    @classmethod
    async def autoDBCount(cls, ctx:discord.Interaction, serverID:str, userID:str) -> None:
        SaveDataUtil.initUser(dataUser, userID, DefaultUserEnum.NORMAL, serverID)
        _dataUser:Dict[str, Any] = dataUser.get(serverID=serverID, userID=userID)
        _dataUser['db_count'] += 1
        dataUser.set(_dataUser, serverID, userID)
        
        SaveDataUtil.initUser(dataUserAchievement, userID, DefaultUserEnum.ACHIEVEMENT, serverID)
        allAchievement:Dict[str, AchievementContent] = getAchievementData()
        _dataUserAchievement:Dict[str, Any] = dataUserAchievement.get(serverID=serverID, userID=userID)
        speaks:Dict[str, int] = {
            speak: cast(int, achievementContent['required'])
            for speak, achievementContent in allAchievement.items()
            if speak.startswith('speak')
        }
        
        for speak, required in speaks.items():
            if _dataUser['db_count'] >= required and not _dataUserAchievement[speak]:
                _dataUserAchievement[speak] = True
                await cls.achievementUnlockMessage(ctx, '대화 업적', allAchievement[speak]['name'], '_h' in speak)
                
        dataUserAchievement.set(_dataUserAchievement, serverID, userID)
        
    @classmethod
    async def autoACCount(cls, ctx:discord.Interaction, serverID:str, userID:str) -> None:
        _dataUser:Dict[str, Any] = dataUser.get(serverID=serverID, userID=userID)
        acTime:int = _dataUser['ac_time']
        acContinuousTime:int = _dataUser['continuous_ac_time']
        
        SaveDataUtil.initUser(dataUserAchievement, userID, DefaultUserEnum.ACHIEVEMENT, serverID)
        allAchievement:Dict[str, AchievementContent] = getAchievementData()
        _dataUserAchievement:Dict[str, Any] = dataUserAchievement.get(serverID=serverID, userID=userID)
        acs:Dict[str, int] = {
            ac: cast(int, achievementContent['required'])
            for ac, achievementContent in allAchievement.items()
            if ac.startswith('ac') and not ac.endswith('_h')
        }
        acContinuouss:Dict[str, int] = {
            ac: cast(int, achievementContent['required'])
            for ac, achievementContent in allAchievement.items()
            if ac.startswith('continuous_ac')
        }
        acHidden:Dict[str, int] = cast(Dict[str, int], allAchievement['ac_h']['required'])
        
        for ac, required in acs.items():
            if acTime >= required and not _dataUserAchievement[ac]:
                _dataUserAchievement[ac] = True
                await cls.achievementUnlockMessage(ctx, '출석 업적', allAchievement[ac]['name'])
        for ac, required in acContinuouss.items():
            if acContinuousTime >= required and not _dataUserAchievement[ac]:
                _dataUserAchievement[ac] = True
                await cls.achievementUnlockMessage(ctx, '출석 업적', allAchievement[ac]['name'])
        if (acTime >= acHidden['ac_time'] or acContinuousTime >= acHidden['continuous_ac_time']) and not _dataUserAchievement['ac_h']:
            _dataUserAchievement['ac_h'] = True
            await cls.achievementUnlockMessage(ctx, '출석 업적', allAchievement['ac_h']['name'], True)
                
        dataUserAchievement.set(_dataUserAchievement, serverID, userID)
        
    @classmethod
    async def autoWalletCount(cls, ctx:discord.Interaction, serverID:str, userID:str) -> None:
        _dataUser:Dict[str, Any] = dataUser.get(serverID=serverID, userID=userID)
        balance:int = _dataUser['balance']

        SaveDataUtil.initUser(dataUserAchievement, userID, DefaultUserEnum.ACHIEVEMENT, serverID)
        allAchievement:Dict[str, AchievementContent] = getAchievementData()
        _dataUserAchievement:Dict[str, Any] = dataUserAchievement.get(serverID=serverID, userID=userID)
        wallets:Dict[str, int] = {
            key: cast(int, content['required'])
            for key, content in allAchievement.items()
            if key.startswith('wallet')
        }

        for wallet, required in wallets.items():
            isExact = (wallet == 'wallet_h1')
            if ((isExact and balance == required) or (not isExact and balance >= required)) and not _dataUserAchievement[wallet]:
                _dataUserAchievement[wallet] = True
                await cls.achievementUnlockMessage(ctx, '잔액 업적', allAchievement[wallet]['name'], '_h' in wallet)

        dataUserAchievement.set(_dataUserAchievement, serverID, userID)