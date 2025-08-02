from library.preimport import *
from library.utils.LevelUtil import *
from library.utils.WalletUtil import *
from library.utils.GambleUtil import *
from library.utils.IntroductionUtil import *
from library.objects.ArrowButt import *
from datetime import timedelta, date
from numpy import log2

GOLD_MEDAL:Literal['🥇'] = '🥇'
SILVER_MEDAL:Literal['🥈'] = '🥈'
COPPER_MEDAL:Literal['🥉'] = '🥉'

def medalChecker(i:int) -> Literal['🥇', '🥈', '🥉', '']:
    return GOLD_MEDAL if i == 0 else SILVER_MEDAL if i == 1 else COPPER_MEDAL if i == 2 else ''

class RankingTypeEnum(BaseEnum):
    ALL = 0
    LEVEL = 1
    MONEY = 2
    GAMBLE = 3
    
def rankingAllScore(*, level:int, xp:int, winNum:int, loseNum:int, tieNum:int, money:int) -> int | float:
    levelResult:int = level * 5
    xpResult:float = xp * (10 ** -len(str(xp)))
    winningRate:int | float = GambleUtil.calcWinningRate(winNum, loseNum, tieNum)
    gambleAllPlayResult:int = GambleUtil.calcAllPlayCount(winNum, loseNum, tieNum) - (tieNum // 2) - loseNum
    moneyResult:int = money // WalletUtil.BASE_EARN
    
    result:int | float = levelResult + xpResult + winningRate + gambleAllPlayResult + moneyResult
    
    if not result.is_integer():
        return round(result, 2)
    return int(result)
        
def rankingGenerator(rankingType:Union[int, RankingTypeEnum], serverID:str) -> List[Tuple[str, Dict[str, Any]]]:
    if isinstance(rankingType, int):
        _rankingType:RankingTypeEnum = cast(RankingTypeEnum, RankingTypeEnum.from_any(rankingType))
    else:
        _rankingType:RankingTypeEnum = rankingType
        
    data:List[Tuple[str, Dict[str, Any]]]
    key:Callable[[Tuple[str, Dict[str, Any]]], Any]
    if _rankingType == RankingTypeEnum.ALL:
        dataPerfect: Dict[str, Dict[str, Any]] = {}
        datas = [dataUser, dataUserGamble]

        for _data in datas:
            for userID, userData in _data.getUsers(serverID).items():
                if userID not in dataPerfect:
                    dataPerfect[userID] = {}
                SaveDataUtil.deepMergeDict(dataPerfect[userID], userData)
                
        data = list(dataPerfect.items())
        key = lambda data: rankingAllScore(
            level=data[1].get('level', 0),
            xp=data[1].get('xp', 0),
            winNum=data[1].get('wins', 0),
            loseNum=data[1].get('loses', 0),
            tieNum=data[1].get('ties', 0),
            money=data[1].get('balance', 0)
        )
        
    elif _rankingType == RankingTypeEnum.LEVEL:
        data = list(dataUser.getUsers(serverID).items())
        key = lambda data: (data[1].get('level', 0), data[1].get('xp', 0))
        
    elif _rankingType == RankingTypeEnum.MONEY:
        data = list(dataUser.getUsers(serverID).items())
        key = lambda data: data[1].get('balance', 0)
        
    elif _rankingType == RankingTypeEnum.GAMBLE:
        data = list(dataUserGamble.getUsers(serverID).items())
        key = lambda data: (
            data[1].get('wins', 0),
            GambleUtil.calcAllPlayCount(data[1].get('wins', 0), data[1].get('loses', 0), data[1].get('ties', 0)),
            GambleUtil.calcWinningRate(data[1].get('wins', 0), data[1].get('loses', 0), data[1].get('ties', 0))
        )
        
    dataSorted:List[Tuple[str, Dict[str, Any]]] = sorted(
        data,
        key=key,
        reverse=True
    )
    return dataSorted

def rankingPage(*, bot:Bot, ctx:Interaction, page:Union[int, RankingTypeEnum], server:Guild, serverID:str, rankingTypeLen:int, now:datetime) -> Embed:
    if isinstance(page, int):
        _page:RankingTypeEnum = cast(RankingTypeEnum, RankingTypeEnum.from_any(page))
    else:
        _page:RankingTypeEnum = page
        
    if _page == RankingTypeEnum.ALL:
        rankingType = '전체'
    elif _page == RankingTypeEnum.LEVEL:
        rankingType = '레벨'
    elif _page == RankingTypeEnum.MONEY:
        rankingType = '잔액'
    elif _page == RankingTypeEnum.GAMBLE:
        rankingType = '사행성'
        
    defaultTitle:str = '`{serverName}` 서버의 {rankingType} 랭킹 (상위 10위)'
    defaultFooter:str = '{rankingTypeLen}페이지 중 {page}페이지'
        
    embed:Embed = Embed(
        title=defaultTitle.format(serverName=server.name, rankingType=rankingType),
        color=NormalUtil.EAGLE_COLOR,
        timestamp=now
    )
    embed.set_thumbnail(url=server.icon.url if server.icon else ctx.user.default_avatar.url)
    
    if _page == RankingTypeEnum.ALL:
        dataSorted:List[Tuple[str, Dict[str, Any]]] = rankingGenerator(RankingTypeEnum.ALL, serverID)
    elif _page == RankingTypeEnum.LEVEL:
        dataSorted:List[Tuple[str, Dict[str, Any]]] = rankingGenerator(RankingTypeEnum.LEVEL, serverID)
    elif _page == RankingTypeEnum.MONEY:
        dataSorted:List[Tuple[str, Dict[str, Any]]] = rankingGenerator(RankingTypeEnum.MONEY, serverID)
    elif _page == RankingTypeEnum.GAMBLE:
        dataSorted:List[Tuple[str, Dict[str, Any]]] = rankingGenerator(RankingTypeEnum.GAMBLE, serverID)
    
    for i, (userID, data) in enumerate(dataSorted[:min(10, len(dataSorted))]):
        user:discord.User = cast(discord.User, bot.get_user(int(userID)))
        name:str = f'{medalChecker(i)}{i + 1}위 - `{user.display_name}`님'
        value:str = ""
        
        if _page == RankingTypeEnum.ALL:
            score:int | float = rankingAllScore(
                level=data.get('level', 0),
                xp=data.get('xp', 0),
                winNum=data.get('wins', 0),
                loseNum=data.get('loses', 0),
                tieNum=data.get('ties', 0),
                money=data.get('balance', 0)
            )
            value = f"총 점수: **{score}**점"
            
        elif _page == RankingTypeEnum.LEVEL:
            thresholdsUser:List[float] = LevelUtil.makeThresholds(data.get('level', 0), 'user')
            bars:List[str] = LevelUtil.makeXPBar()
            xpBarUser:str = bars[bisect.bisect(thresholdsUser, data.get('xp', 0))]
            value = (
                f"레벨: **{data.get('level', 0)}**\n"
                f"경험치: **{data.get('xp', 0)}/{LevelUtil.calcLevelXPTotal(data.get('level', 0), 'user')}**\n"
                f"{xpBarUser}"
            )
            
        elif _page == RankingTypeEnum.MONEY:
            value = f"잔액: **{data.get('balance', 0)}**원\n"
            
        elif _page == RankingTypeEnum.GAMBLE:
            value = (
                f"승률: **{GambleUtil.calcWinningRate(data.get('wins', 0), data.get('loses', 0), data.get('ties', 0))}**%\n"
                f"(총 플레이 횟수: **{GambleUtil.calcAllPlayCount(data.get('wins', 0), data.get('loses', 0), data.get('ties', 0))}**회, 승리 횟수: **{data.get('wins', 0)}**회, 패배 횟수: **{data.get('loses', 0)}**회, 비긴 횟수: **{data.get('ties', 0)}**회)"
            )
        
        embed.add_field(
            name=name,
            value=value,
            inline=False
        )
        
    if len(dataSorted) == 0:
        embed.add_field(
            name='...?',
            value="*아무도 이 컨텐츠에 대해 참여하지 않았어요 🤔*",
            inline=False
        )
        
    embed.set_footer(text=defaultFooter.format(rankingTypeLen=rankingTypeLen, page=_page.value + 1))
    
    return embed

def rankingCallbackGenerator(*, bot:Bot, ctx:Interaction, view:BaseButt, callbackType:Literal['left', 'middle', 'right'], server:Guild, serverID:str, rankingTypeLen:int, now:datetime) -> BUTT_CALLBACK_TYPE:
    add:Literal[1, -1] = -1 if callbackType == 'left' else 1
    minValue:int = 0
    maxValue:int = rankingTypeLen - 1
    async def callback(interaction:Interaction):
        view.initProperty('page', 0)
            
        view.setProperty('page', view.getProperty('page') + add)
        if callbackType == 'middle':
            view.setProperty('page', random.randint(minValue, maxValue))
        elif callbackType == 'left' and view.getProperty('page') < minValue:
            view.setProperty('page', maxValue)
        elif not callbackType == 'left' and view.getProperty('page') > maxValue:
            view.setProperty('page', minValue)
        
        await interaction.response.edit_message(embed=rankingPage(
            bot=bot,
            ctx=ctx,
            page=view.getProperty('page'),
            server=server,
            serverID=serverID,
            rankingTypeLen=rankingTypeLen,
            now=now
        ))
        
    return callback

class InfoTypeEnum(BaseEnum):
    INFO = 0
    RANKING = 1
    INTRODUCTION = 2
    
def infoPage(
        *,
        member:Member,
        page:Union[int, InfoTypeEnum] = InfoTypeEnum.INFO,
        dataUser:Dict[str, Any],
        dataUserIntroduction:Dict[str, str],
        levelContent:Dict[Literal['base_user_xp', 'xp_bar_user'], str | int],
        gambleContent:Dict[Literal['winning_rate', 'all_play_count', 'wins', 'loses', 'ties'], int | float],
        serverAndETCContent:Dict[Literal['server_name', 'is_member_sponsor', 'how_long_been_server', 'ac_time', 'ac_continuous_time'], str | int | bool | List[Member]],
        now:datetime
    ) -> Embed:
    title:str = f'`{member.display_name}`님의 정보'
    content:str | None = None
    defaultFooter:str = '{rankingTypeLen}페이지 중 {page}페이지'
    
    if isinstance(page, int):
        _page:InfoTypeEnum = cast(InfoTypeEnum, InfoTypeEnum.from_any(page))
    else:
        _page:InfoTypeEnum = page
    
    if _page == InfoTypeEnum.INTRODUCTION:
        title = dataUserIntroduction['title'] if NormalUtil.objNullChecks(False, title=dataUserIntroduction['title']) else f'`{member.display_name}`님의 소개문...?'
        content = dataUserIntroduction['content'] if NormalUtil.objNullChecks(False, content=dataUserIntroduction['content']) else "안타깝게도 이 분이 소개문을 작성하지 않았어요 :("
    elif _page == InfoTypeEnum.RANKING:
        title = f'`{member.display_name}`님의 `{member.guild.name}` 랭킹'
        
    embed:Embed = Embed(
        title=title,
        description=content,
        color=NormalUtil.EAGLE_COLOR,
        timestamp=now
    )
    embed.set_thumbnail(url=member.display_avatar.url)
        
    if _page == InfoTypeEnum.INFO:
        embed.add_field(
            name='경험치 및 레벨',
            value=(
                f"레벨: **{dataUser['level']}**\n"
                f"경험치: **{dataUser['xp']}/{levelContent['base_user_xp']}**\n"
                f"{levelContent['xp_bar_user']}"
            ),
            inline=False
        )
        embed.add_field(
            name='잔액',
            value=f"**{dataUser['balance']}원**",
            inline=False
        )
        embed.add_field(
            name='사행성',
            value=(
                f"승률: **{gambleContent['winning_rate']}%**\n"
                f"총 플레이 횟수: **{gambleContent['all_play_count']}회**\n"
                f"이긴 횟수: **{gambleContent['wins']}회**\n"
                f"진 횟수: **{gambleContent['loses']}회**\n"
                f"비긴 횟수: **{gambleContent['ties']}회**\n"
            ),
            inline=False
        )
        embed.add_field(
            name='기타',
            value=(
                f"출석 횟수: **{serverAndETCContent['ac_time']}회{' (' + str(serverAndETCContent['ac_continuous_time']) + '연속 출석)' if cast(int, serverAndETCContent['ac_continuous_time']) > 1 else ''}**"
            ),
            inline=False
        )

        if serverAndETCContent['is_member_sponsor']:
            embed.add_field(
                name=f'✨`{serverAndETCContent["server_name"]}` 서버 후원자!✨',
                value=f"**이 분은 무려 `{serverAndETCContent['server_name']}` 서버를 부스트를 한 적이 있어요!**",
                inline=False
            )
            
        embed.add_field(
            name='서버에 들어온 날짜',
            value=f"`{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}`" if member.joined_at else "잘 모르겠어요 :(",
            inline=True
        )
        embed.add_field(
            name='서버에서 몇번째',
            value=f'{cast(List[Member], serverAndETCContent["how_long_been_server"]).index(member) + 1}번째',
            inline=True
        )
    elif _page == InfoTypeEnum.RANKING:
        defaultName:str = '{rankingType} 랭킹 - {rank}'
        for rankingIndex in range(RankingTypeEnum.getItemLength()):
            dataSorted:List[Tuple[str, Dict[str, Any]]] = rankingGenerator(rankingIndex, serverID=str(member.guild.id))
            rankingType:RankingTypeEnum = cast(RankingTypeEnum, RankingTypeEnum.from_any(rankingIndex))

            userRank:int | None = next((idx for idx, (userID, data) in enumerate(dataSorted) if userID == str(member.id)), None)
            _userRank:int = -1 if userRank is None else userRank
            name:str = ''
            value:str = '*이 분은 이 콘텐츠에 아직 참여하지 않으셨어요!*'
            if rankingType == RankingTypeEnum.ALL:
                name = '전체'
            elif rankingType == RankingTypeEnum.LEVEL:
                name = '레벨'
            elif rankingType == RankingTypeEnum.MONEY:
                name = '잔액'
            elif rankingType == RankingTypeEnum.GAMBLE:
                name = '사행성'
                
            if _userRank != -1:
                userData:Dict[str, Any] = dataSorted[_userRank][1]

                if rankingType == RankingTypeEnum.ALL:
                    score:int | float = rankingAllScore(
                        level=userData.get('level', 0),
                        xp=userData.get('xp', 0),
                        winNum=userData.get('wins', 0),
                        loseNum=userData.get('loses', 0),
                        tieNum=userData.get('ties', 0),
                        money=userData.get('balance', 0)
                    )
                    value = f"총 점수: **{score}점**"

                elif rankingType == RankingTypeEnum.LEVEL:
                    level:int = userData.get('level', 0)
                    xp:int = userData.get('xp', 0)
                    baseUserXP:int = LevelUtil.calcLevelXPTotal(level, 'user')
                    thresholdsUser:List[float] = LevelUtil.makeThresholds(level, 'user')
                    bars:List[str] = LevelUtil.makeXPBar()
                    xpBarUser:str = bars[bisect.bisect(thresholdsUser, userData.get('xp', 0))]
                    value = (
                        f"레벨: **{level}**\n"
                        f"경험치: **{xp}/{baseUserXP}**\n"
                        f"{xpBarUser}\n"
                    )

                elif rankingType == RankingTypeEnum.MONEY:
                    value = f"잔액: **{userData.get('balance', 0)}**원"

                elif rankingType == RankingTypeEnum.GAMBLE:
                    wins:int = userData.get('wins', 0)
                    loses:int = userData.get('loses', 0)
                    ties:int = userData.get('ties', 0)
                    winRate:int | float = GambleUtil.calcWinningRate(wins, loses, ties)
                    allPlayCount:int = GambleUtil.calcAllPlayCount(wins, loses, ties)
                    value = (
                        f"승률: **{winRate}**%\n"
                        f"(총 플레이 횟수: **{allPlayCount}**회, 승리 횟수: **{wins}**회, 패배 횟수: **{loses}**회, 비긴 횟수: **{ties}**회)"
                    )

            rank:str = f'{medalChecker(_userRank)}{_userRank + 1}위' if _userRank != -1 else '랭크 없음'
            embed.add_field(
                name=defaultName.format(rankingType=name, rank=rank),
                value=value,
                inline=False
            )
    
    embed.set_footer(text=defaultFooter.format(rankingTypeLen=InfoTypeEnum.getItemLength(), page=_page.value + 1))
    
    return embed

def infoCallbackGenerator(
        view:BaseButt, isLeft:bool,
        *,
        member:Member,
        dataUser:Dict[str, Any],
        dataUserIntroduction:Dict[str, str],
        levelContent:Dict[Literal['base_user_xp', 'xp_bar_user'], str | int],
        gambleContent:Dict[Literal['winning_rate', 'all_play_count', 'wins', 'loses', 'ties'], int | float],
        serverAndETCContent:Dict[Literal['server_name', 'is_member_sponsor', 'how_long_been_server', 'ac_time', 'ac_continuous_time'], str | int | bool | List[Member]],
        now:datetime
    ) -> BUTT_CALLBACK_TYPE:
    add:Literal[1, -1] = -1 if isLeft else 1
    minValue:int = 0
    maxValue:int = InfoTypeEnum.getItemLength() - 1
    async def callback(interaction:Interaction):
        view.initProperty('page', 0)
            
        view.setProperty('page', view.getProperty('page') + add)
        if isLeft and view.getProperty('page') < minValue:
            view.setProperty('page', maxValue)
        elif not isLeft and view.getProperty('page') > maxValue:
            view.setProperty('page', minValue)
        
        await interaction.response.edit_message(embed=infoPage(
            member=member,
            page=view.getProperty('page'),
            dataUser=dataUser,
            dataUserIntroduction=dataUserIntroduction,
            levelContent=levelContent,
            gambleContent=gambleContent,
            serverAndETCContent=serverAndETCContent,
            now=now
        ))
        
    return callback

class NormalCog(commands.Cog):
    bot:Bot
    
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @app_commands.command(name='핑', description="봇의 반응속도를 확인할 수 있습니다.")
    async def ping(self, ctx:Interaction):
        NOW:datetime = datetime.now()
        if not NormalUtil.isUser(self.bot.user):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW))
            ErrorUtil.runError(ErrorEmbedType.BOT_LOGOUTED, NOW)
        if not NormalUtil.isInteractionServer(ctx.guild):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW))
            try:
                ErrorUtil.runError(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW)
            except SmallError:
                return

        serverID:str = str(ctx.guild.id)
        userID:str = str(ctx.user.id)
        
        pong:str = random.choice([
            "퐁!",
            "퐁! 저 아직 살아있어요!",
            "핑!",
        ])
        thresholds:List[int] = [200, 250, 300, 400]
        messages:List[str] = [
            "아주 좋음!",
            "좋음!",
            "보통",
            "나쁨",
            "`:(`"
        ]

        curLatency:float = self.bot.latency * 1000
        latencyText:str = messages[bisect.bisect(thresholds, curLatency)]
        
        embed:Embed = Embed(
            title=pong,
            color=NormalUtil.EAGLE_COLOR,
            timestamp=NOW
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(name='딜레이', value=f"`{curLatency:.2f}`ms ({latencyText})", inline=False)
        embed.add_field(name='부팅 일자', value=f"`{NormalUtil.BOOTING_TIME.strftime('%Y-%m-%d %H:%M:%S')}`", inline=False)

        await ctx.response.send_message(embed=embed)
        
        SaveDataUtil.initUser(dataUserAchievement, userID, DefaultUserEnum.ACHIEVEMENT, serverID)
        data:Dict[str, bool] = dataUserAchievement.get(serverID=serverID, userID=userID)
        if not data['ping']:
            data['ping'] = True
            await AchievementUtil.achievementUnlockMessage(ctx, '평범한 업적', '핑!')
            
            dataUserAchievement.set(data, serverID, userID)
            
        await AchievementUtil.autoDBCount(ctx, serverID, userID)
            
    @app_commands.command(name='출석체크', description="출석체크를 해봅시다.")
    async def attendanceCheck(self, ctx:Interaction):
        NOW:datetime = datetime.now()
        if not NormalUtil.isInteractionServer(ctx.guild):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW))
            try:
                ErrorUtil.runError(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW)
            except SmallError:
                return

        await ctx.response.defer(thinking=True)
        
        serverID:str = str(ctx.guild.id)
        userID:str = str(ctx.user.id)
        LISTED_TODAY:List[int] = [NOW.month, NOW.day]
        CUR_FORMATED_DATE:str = NOW.strftime('%Y-%m-%d %H:%M:%S')
        YESTERDAY:date = NOW.date() - timedelta(days=1)
        LISTED_YESTERDAY:List[int] = [YESTERDAY.month, YESTERDAY.day]
        
        SaveDataUtil.initUser(dataUser, userID, DefaultUserEnum.NORMAL, serverID)
        SaveDataUtil.initServer(dataServer, serverID, DefaultServerEnum.NORMAL)
        
        _dataUser:Dict[str, Any] = dataUser.get(serverID=serverID, userID=userID)
        _dataServer:Dict[str, Any] = dataServer.get(serverID=serverID)
        lastClaimDay:List[int] = _dataUser['date']
        isMemberSponsor:bool = ctx.user in ctx.guild.premium_subscribers
        
        if lastClaimDay == LISTED_TODAY:
            await ctx.followup.send(f"`{ctx.user.display_name}`님은 오늘 이미 출석체크를 했어요!", ephemeral=True)
            return
        
        if lastClaimDay == LISTED_YESTERDAY:
            _dataUser['continuous_ac_time'] += 1
        else:
            _dataUser['continuous_ac_time'] = 1
            
        calcedXP:int = LevelUtil.calcXP(_dataUser['continuous_ac_time'])
        calcedContinuousXP:int = 0
        calcedContinuousMoney:int = 0
        
        _dataServer['xp'] += calcedXP
        _dataUser['xp'] += calcedXP
        _dataServer['balance'] += WalletUtil.BASE_EARN
        _dataUser['balance'] += WalletUtil.BASE_EARN
        
        _dataUser['date'] = LISTED_TODAY
        _dataUser['ac_time'] += 1
        
        if _dataUser['continuous_ac_time'] > 1:
            calcedContinuousXP = int(log2(_dataUser['continuous_ac_time']) * LevelUtil.XP_INCREASE_MULT)
            calcedContinuousMoney = int(log2(_dataUser['continuous_ac_time']) * 100)
            _dataServer['xp'] += calcedContinuousXP
            _dataUser['xp'] += calcedContinuousXP
            _dataServer['balance'] += calcedContinuousMoney
            _dataUser['balance'] += calcedContinuousMoney
        
        if isMemberSponsor:
            _dataUser['xp'] += 10
            _dataServer['xp'] += 10
            _dataServer['balance'] += 1000
            _dataUser['balance'] += 1000
        
        baseServerXP:int = LevelUtil.calcLevelXPTotal(_dataUser['level'], 'server')
        baseUserXP:int = LevelUtil.calcLevelXPTotal(_dataUser['level'], 'user')
        isLevelUpServer:bool = LevelUtil.isLevelIncrease(_dataServer['xp'], baseServerXP)
        isLevelUpUser:bool = LevelUtil.isLevelIncrease(_dataUser['xp'], baseUserXP)
        
        if isLevelUpServer:
            _dataServer['xp'] -= baseServerXP
            _dataServer['level'] += 1
        
        if isLevelUpUser:
            _dataUser['xp'] -= baseUserXP
            _dataUser['level'] += 1
            
        dataServer.set(_dataServer, serverID=serverID)
        dataUser.set(_dataUser, serverID=serverID, userID=userID)
        
        thresholdsServer:List[float] = LevelUtil.makeThresholds(_dataUser['level'], 'server')
        thresholdsUser:List[float] = LevelUtil.makeThresholds(_dataUser['level'], 'user')

        bars:List[str] = LevelUtil.makeXPBar()
        
        xpBarServer:str = bars[bisect.bisect(thresholdsServer, _dataServer['xp'])]
        xpBarUser:str = bars[bisect.bisect(thresholdsUser, _dataUser['xp'])]
        
        continuousACText:str = f'{_dataUser["continuous_ac_time"]}연속 ' if _dataUser['continuous_ac_time'] > 1 else ''
        continuousXPText:str = f' (+ {calcedContinuousXP}xp 연속 출석 보너스!)' if calcedContinuousXP else ''
        premiumXPText:str = ' (+ 10xp 서버 부스트 보너스!)' if isMemberSponsor else ''
        continuousMoneyText:str = f' (+ {calcedContinuousMoney}원 연속 출석 보너스!)' if calcedContinuousMoney else ''
        premiumMoneyText:str = ' (+ 1000원 서버 부스트 보너스!)' if isMemberSponsor else ''
        
        levelUpServerText:str = f"{_dataServer['level'] - 1} -> {_dataServer['level']}" if isLevelUpServer else _dataServer['level']
        levelUpUserText:str = f"{_dataUser['level'] - 1} -> {_dataUser['level']}" if isLevelUpUser else _dataUser['level']
        
        embed:Embed = Embed(
            title=f'`{ctx.user.display_name}`님의 {_dataUser["ac_time"]}번째 {continuousACText}출석체크가 완료되었습니다! ✨',
            description=f'(`{CUR_FORMATED_DATE}`에 출석체크됨)',
            color=NormalUtil.EAGLE_COLOR,
            timestamp=NOW
        )
        embed.set_thumbnail(url=ctx.user.display_avatar.url)
        embed.add_field(
            name=f'**`{ctx.guild.name}` 서버**',
            value=(
                f"레벨: **{levelUpServerText}**\n"
                f"경험치: **{_dataServer['xp']}/{baseServerXP}{continuousXPText}{premiumXPText}**\n"
                f"{xpBarServer}"
            ),
            inline=False
        )
        embed.add_field(
            name=f'**`{ctx.user.display_name}`님**',
            value=(
                f"레벨: **{levelUpUserText}**\n"
                f"경험치: **{_dataUser['xp']}/{baseUserXP}{continuousXPText}{premiumXPText}**\n"
                f"{xpBarUser}"
            ),
            inline=False
        )
        embed.add_field(
            name='**획득 보상**',
            value=(
                f"돈: **{WalletUtil.BASE_EARN}{continuousMoneyText}{premiumMoneyText}원**"
            ),
            inline=False
        )
        
        await ctx.followup.send(embed=embed)
        
        await AchievementUtil.autoDBCount(ctx, serverID, userID)
        await AchievementUtil.autoACCount(ctx, serverID, userID)
        await AchievementUtil.autoWalletCount(ctx, serverID, userID)
        
    @app_commands.command(name='유저정보', description="서버에 있는 사람들의 정보를 확인합니다.")
    @app_commands.rename(member='user')
    @app_commands.describe(member="(확인하고픈 유저를 골라주세요, 만일 고르지 않을 경우 자신의 정보가 나옵니다.)")
    async def userInfo(self, ctx:Interaction, member:discord.Member | None = None):
        NOW:datetime = datetime.now()
        if not NormalUtil.isUser(self.bot.user):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW))
            ErrorUtil.runError(ErrorEmbedType.BOT_LOGOUTED, NOW)
        if not NormalUtil.isInteractionServer(ctx.guild):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW))
            try:
                ErrorUtil.runError(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW)
            except SmallError:
                return

        await ctx.response.defer(thinking=True)
        
        _member:Member = cast(Member, ctx.user) if member == None else member
            
        if _member.display_name == self.bot.user.display_name:
            await ctx.followup.send(embed=IntroductionUtil.getEagleIntroduction(self.bot))
            return
        
        elif _member.bot:
            await ctx.followup.send(
                "봇의 정보를 확인하는 건 `전국 디스코드 봇 협회`에 의해 불가능해요!\n"
                "~~(그리고 다른 봇의 정보를 확인하는 건 구글이 더 낫지 않을까요...?)~~"
            )
            return
        
        guild:Guild = ctx.guild
        serverID:str = str(ctx.guild.id)
        userID:str = str(_member.id)
        
        SaveDataUtil.initUser(dataUser, userID, DefaultUserEnum.NORMAL, serverID)
        SaveDataUtil.initUser(dataUserGamble, userID, DefaultUserEnum.GAMBLE, serverID)
        SaveDataUtil.initUser(dataUserIntroduction, userID, DefaultUserEnum.INTRODUCTION)
        
        _dataUser:Dict[str, Any] = dataUser.get(serverID=serverID, userID=userID)
        _dataUserGamble:Dict[str, Any] = dataUserGamble.get(serverID=serverID, userID=userID)
        _dataUserIntroduction:Dict[str, str] = dataUserIntroduction.get(userID=userID)
            
        baseUserXP:int = LevelUtil.calcLevelXPTotal(_dataUser['level'], 'user')
        howLongBeenServer:List[Member] = sorted(guild.members, key=lambda member: member.joined_at or guild.created_at)
        winningRate:int | float = GambleUtil.calcWinningRate(_dataUserGamble['wins'], _dataUserGamble['loses'], _dataUserGamble['ties'])
        wins:int = _dataUserGamble['wins']
        loses:int = _dataUserGamble['loses']
        ties:int = _dataUserGamble['ties']
        allPlayCount:int = GambleUtil.calcAllPlayCount(wins, loses, ties)
        
        thresholdsUser:List[float] = LevelUtil.makeThresholds(_dataUser['level'], 'user')
        bars:List[str] = LevelUtil.makeXPBar()
        xpBarUser:str = bars[bisect.bisect(thresholdsUser, _dataUser['xp']) - 1]
        
        serverName:str = guild.name
        acTime:int = _dataUser['ac_time']
        acContinuousTime:int = _dataUser['continuous_ac_time']
        isMemberSponsor:bool = _member in _member.guild.premium_subscribers
                
        view:ArrowButt = ArrowButt(
            ctx,
            left={
                'label': '←',
                'row': 0,
                'style': ButtonStyle.success,
                'disable': False
            },
            right={
                'label': '→',
                'row': 0,
                'style': ButtonStyle.success,
                'disable': False
            }
        )
        
        def callbackGenerator(isLeft:bool) -> BUTT_CALLBACK_TYPE:
            return infoCallbackGenerator(
                view, isLeft,
                member=_member,
                dataUser=_dataUser,
                dataUserIntroduction=_dataUserIntroduction,
                levelContent={
                    'base_user_xp': baseUserXP,
                    'xp_bar_user': xpBarUser,
                },
                gambleContent={
                    'winning_rate': winningRate,
                    'all_play_count': allPlayCount,
                    'wins': wins,
                    'loses': loses,
                    'ties': ties
                },
                serverAndETCContent={
                    'server_name': serverName,
                    'is_member_sponsor': isMemberSponsor,
                    'how_long_been_server': howLongBeenServer,
                    'ac_time': acTime,
                    'ac_continuous_time': acContinuousTime
                },
                now=NOW
            )

        view.leftCallback = callbackGenerator(True)
        view.rightCallback = callbackGenerator(False)
                
        await ctx.followup.send(
            embed=infoPage(
                member=_member,
                page=0,
                dataUser=_dataUser,
                dataUserIntroduction=_dataUserIntroduction,
                levelContent={
                    'base_user_xp': baseUserXP,
                    'xp_bar_user': xpBarUser,
                },
                gambleContent={
                    'winning_rate': winningRate,
                    'all_play_count': allPlayCount,
                    'wins': wins,
                    'loses': loses,
                    'ties': ties
                },
                serverAndETCContent={
                    'server_name': serverName,
                    'is_member_sponsor': isMemberSponsor,
                    'how_long_been_server': howLongBeenServer,
                    'ac_time': acTime,
                    'ac_continuous_time': acContinuousTime
                },
                now=NOW
            ),
            view=view
        )
        
        await AchievementUtil.autoDBCount(ctx, serverID, userID)
        
    @app_commands.command(name='전체유저랭킹', description="서버에 있는 모든 유저의 랭크를 볼 수 있습니다.")
    async def userRanking(self, ctx:Interaction):
        NOW:datetime = datetime.now()
        if not NormalUtil.isUser(self.bot.user):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW))
            ErrorUtil.runError(ErrorEmbedType.BOT_LOGOUTED, NOW)
        if not NormalUtil.isInteractionServer(ctx.guild):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW))
            try:
                ErrorUtil.runError(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW)
            except SmallError:
                return

        await ctx.response.defer(thinking=True)
        
        serverID:str = str(ctx.guild.id)
        userID:str = str(ctx.user.id)
        
        SaveDataUtil.initUser(dataUser, userID, DefaultUserEnum.NORMAL, serverID)
        SaveDataUtil.initServer(dataUserGamble, serverID)
        
        rankingTypeLen:int = RankingTypeEnum.getItemLength()
        
        view:ArrowButt = ArrowButt(
            ctx,
            left={
                'label': '←',
                'row': 0,
                'style': ButtonStyle.success,
                'disable': False
            },
            middle={
                'label': '🎰',
                'row': 0,
                'style': ButtonStyle.success,
                'disable': False
            },
            right={
                'label': '→',
                'row': 0,
                'style': ButtonStyle.success,
                'disable': False
            }
        )
        
        def callbackGenerator(callbackType:Literal['left', 'middle', 'right']):
            return rankingCallbackGenerator(
                bot=self.bot,
                ctx=ctx,
                view=view,
                callbackType=callbackType,
                server=cast(Guild, ctx.guild),
                serverID=serverID,
                rankingTypeLen=rankingTypeLen,
                now=NOW
            )
        
        view.leftCallback = callbackGenerator('left')
        view.middleCallback = callbackGenerator('middle')
        view.rightCallback = callbackGenerator('right')
                
        await ctx.followup.send(
            embed=rankingPage(
                bot=self.bot,
                ctx=ctx,
                page=0,
                server=ctx.guild,
                serverID=serverID,
                rankingTypeLen=rankingTypeLen,
                now=NOW
            ),
            view=view
        )
        
        await AchievementUtil.autoDBCount(ctx, serverID, userID)
    
    @app_commands.command(name='유저소개문작성', description="글로벌한 설명문 폭격기")
    async def userIntroductionMaker(self, ctx:Interaction):
        NOW:datetime = datetime.now()
        if not NormalUtil.isUser(self.bot.user):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW))
            ErrorUtil.runError(ErrorEmbedType.BOT_LOGOUTED, NOW)
        
        userID:str = str(ctx.user.id)
        
        SaveDataUtil.initUser(dataUserIntroduction, userID, DefaultUserEnum.INTRODUCTION)
        
        modal:Modal = Modal(title='소개문 작성기')
        modal.add_item(TextInput(
            label='소개문 제목',
            min_length=4,
            max_length=16,
            style=TextStyle.short,
            placeholder='제목을 입력하세요...'
        ))
        modal.add_item(TextInput(
            label='소개문 내용',
            min_length=10,
            max_length=350,
            style=TextStyle.long,
            placeholder='제목을 입력하세요...'
        ))
        def submitGenerator() -> Callable[[Interaction], Any]:
            async def submit(interaction:Interaction):
                title = modal.children[0]
                content = modal.children[1]
                
                butt:AgreeButt = AgreeButt(interaction)
                async def timeoutCallback(interaction:Interaction):
                    await interaction.edit_original_response(content="3분이 지나 취소되었습니다.", embed=None, view=None)
                butt.timeoutCallback = timeoutCallback
                
                async def agreeCallback(interaction:Interaction):
                    dataUserIntroduction.set({'title': str(title), 'content': str(content)}, userID=userID)
                    await interaction.response.edit_message(
                        content=(
                            f"`{interaction.user.display_name}`님의 소개문이 완성되었습니다!\n"
                            "`/유저정보`로 확인해보세요!"
                        ),
                        embed=None,
                        view=None
                    )
                    butt.timeoutCallback = nothingCallback
                    return
                butt.agreeCallback = agreeCallback
                
                async def declineCallback(interaction:Interaction):
                    await interaction.response.edit_message(
                        content=(
                            f"취소하였습니다.\n"
                            "다시 작성하시려면 `/유저소개문작성`을 입력해주세요."
                        ),
                        embed=None,
                        view=None
                    )
                    return
                butt.declineCallback = declineCallback
                
                embed = discord.Embed(
                    title=f"{title}",
                    description=content,
                    color=discord.Color.from_rgb(139, 69, 19),
                    timestamp=NOW
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                
                await interaction.response.send_message("정말 이대로 만족하십니까?", embed=embed, view=butt, ephemeral=True)
                
            return submit
        
        modal.on_submit = submitGenerator()
        await ctx.response.send_modal(modal)
        
    @app_commands.command(name='업적', description="사실 난 대학에서 업적을 전공했다는 사실")
    @app_commands.rename(member='user')
    @app_commands.describe(member="(확인하고픈 유저를 골라주세요, 만일 고르지 않을 경우 자신의 업적이 나옵니다.)")
    async def achievement(self, ctx:Interaction, member:Member | None = None):
        NOW:datetime = datetime.now()
        if not NormalUtil.isUser(self.bot.user):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW))
            ErrorUtil.runError(ErrorEmbedType.BOT_LOGOUTED, NOW)
        if not NormalUtil.isInteractionServer(ctx.guild):
            await ctx.response.send_message(embed=ErrorUtil.getErrorEmbed(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW))
            try:
                ErrorUtil.runError(ErrorEmbedType.CALLED_FROM_NOT_GUILD, NOW)
            except SmallError:
                return

        await ctx.response.defer(thinking=True)
        
        _member:Member = cast(Member, ctx.user) if member == None else member
            
        serverID:str = str(ctx.guild.id)
        userID:str = str(_member.id)
        
        SaveDataUtil.initUser(dataUserAchievement, userID, DefaultUserEnum.ACHIEVEMENT, serverID)
        currentDataUserAchievement:Dict[str, bool] = dataUserAchievement.get(serverID=serverID, userID=userID)
        achievementData:Dict[str, AchievementContent] = getAchievementData()
        
        embed:Embed = Embed(
            title='분류를 선택해주세요...',
            description="분류를 선택해주세요...",
            color=NormalUtil.EAGLE_COLOR,
            timestamp=NOW
        )
        embed.set_thumbnail(url=_member.display_avatar.url)
        
        combinView:View = View()
        async def timeoutCallback():
            try:
                await ctx.edit_original_response(content="드롭다운은 쌓이면 머리가 아픈 거에요!", embed=None, view=None)
                
            except discord.errors.NotFound:
                pass
            
        combinView.on_timeout = timeoutCallback
        
        bigOptions:List[SelectOption] = [
            discord.SelectOption(label='평범한 업적', description="다른 거에는 관련이 없는 평범한 업적들이에요.", value='normal', emoji='🔖'), # 평범한 녀석들 분류
            discord.SelectOption(label='대화 업적', description="저랑 대화하면 얻어지는 업적들이에요.", value='speak', emoji='🔖'), # 대화 분류
            discord.SelectOption(label='출석 업적', description="출석체크를 하면 얻어지는 업적들이에요.", value='ac', emoji='🔖'), # 출석 분류
            discord.SelectOption(label='잔액 업적', description="돈이 있으면 얻어지는 업적들이에요.", value='wallet', emoji='🔖'), # 잔액 분류
            discord.SelectOption(label='사행성 업적', description="사행성 게임을 하면 얻어지는 업적들이에요.", value='gamble', emoji='🔖'), # 사행성 분류
            discord.SelectOption(label='전투 업적', description="싸우면 얻어지는 업적들이에요.", value='fight', emoji='🔖'), # 전투 분류
            discord.SelectOption(label='컬렉션 업적', description="다른 업적들을 얻으면 얻어지는 업적들이에요.", value='trophy', emoji='🔖'), # 업적 분류
        ]
        
        bigAchievementDropdown:Select = Select(
            placeholder='분류를 선택해주세요...',
            min_values=1,
            max_values=1,
            options=bigOptions
        )
        smallAchievementDropdown:Select = Select(
            placeholder='업적을 선택해주세요...',
            min_values=1,
            max_values=1
        )
        def bigCallbackGenerator() -> Any:
            async def bigCallback(interaction:Interaction):
                bigSelectedValue:str = bigAchievementDropdown.values[0]
                bigSelectedOption:SelectOption = next(
                    (option for option in bigAchievementDropdown.options if option.value == bigSelectedValue),
                    SelectOption(label='error', description='error', value='error')
                )
                
                embed.title = bigSelectedOption.label
                embed.description = bigSelectedOption.description
                
                embed.clear_fields()
                embed.add_field(
                    name='업적을 선택해주세요...',
                    value="업적을 선택해주세요...",
                    inline=False
                )
                
                smallOptions:List[SelectOption] = [
                    SelectOption(
                        label=value['name'],
                        description=(
                            f"{value['description']}\n"
                            f"{'(' + value['plus_description'].format(userName=ctx.user.display_name) + ')' if currentDataUserAchievement[key] else ''}"
                        ),
                        value=key,
                        emoji='✅' if currentDataUserAchievement[key] else '❌'
                    )
                    for key, value in achievementData.items()
                    if value['achievement_area'] == bigSelectedValue
                ]
                smallAchievementDropdown.options = smallOptions
                
                combinView.clear_items()
                combinView.add_item(bigAchievementDropdown)
                combinView.add_item(smallAchievementDropdown)
                
                await interaction.response.edit_message(embed=embed, view=combinView)
                
            return bigCallback
        
        def smallCallbackGenerator() -> Any:
            async def smallCallback(interaction:Interaction):
                smallSelectedValue:str = smallAchievementDropdown.values[0]
                smallSelectedOption:SelectOption = next(
                    (option for option in smallAchievementDropdown.options if option.value == smallSelectedValue),
                    SelectOption(label='error', description='error', value='error')
                )
                
                embed.clear_fields()
                embed.add_field(
                    name=f'{str(smallSelectedOption.emoji)} {smallSelectedOption.label}',
                    value=smallSelectedOption.description,
                    inline=False
                )
                
                await interaction.response.edit_message(embed=embed, view=combinView)
                
            return smallCallback
        
        bigAchievementDropdown.callback = bigCallbackGenerator()
        smallAchievementDropdown.callback = smallCallbackGenerator()
        
        combinView.add_item(bigAchievementDropdown)
        await ctx.followup.send(embed=embed, view=combinView)
        
        await AchievementUtil.autoDBCount(ctx, serverID, userID)