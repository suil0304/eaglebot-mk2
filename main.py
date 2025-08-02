# 디스코드
from discord.ext.commands import Context
# 사용자 지정 모듈들
from library.preimport import *
# Cog
from library.cogs.NormalCog import NormalCog
# 메모리 추적 (왜 있는진 몰?루)
import tracemalloc
# 기타
import os
from dotenv import load_dotenv
tracemalloc.start()
os.system('cls')

load_dotenv()

intents:discord.Intents = discord.Intents.all()
bot:Bot = Bot(command_prefix='!', intents=intents)

TERMINAL_CLEAR_INTERVAL:int = 3600
curClearTime:float = time.time()

async def loofTerminalClear():
    global curClearTime
    await bot.wait_until_ready()
    while not bot.is_closed():
        newClearTime:float = time.time()
        if newClearTime - curClearTime >= TERMINAL_CLEAR_INTERVAL:
            curClearTime = newClearTime
            os.system('cls')
        await asyncio.sleep(600)

# 아주 기밀
# TOKEN:str = "Put your discord bot token"
TOKEN:str = os.getenv("DISCORD_TOKEN")
    
@bot.event
async def on_ready():
    userBot:ClientUser | None = bot.user
    userBotID:int | None = bot.user.id if bot.user else None
    print(f'Logged in as {userBot} (ID: {userBotID})')
    print('------')

    await bot.add_cog(NormalCog(bot), override=True)

    await bot.tree.sync()

    await bot.change_presence(activity=discord.Activity(
        name='아무 거나',
        type=discord.ActivityType.playing,
    ))
    
    bot.loop.create_task(loofTerminalClear())
    
# 서버에 봇이 들어갔을 때
# @bot.event
# async def on_guild_join(guild:Guild):
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             async with channel.typing():
#                 embed = await asyncio.to_thread(createJoinEmbed, bot)
#                 await channel.send(embed=embed)
            
#             break
        
# def createJoinEmbed(bot:Bot) -> Embed:
#     NOW:datetime = datetime.now()
#     if not NormalUtil.isUser(bot.user):
#         return ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW)
        
#     embed:Embed = Embed(
#         title="안녕하세요! 입니다!",
#         description="전 간단하지만 재밌는 기능들을 포함한 디스코드 봇이에요!\n제 명령어는요...",
#         color=NormalUtil.EAGLE_COLOR,
#         timestamp=NOW
#     )
#     embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)

#     명령어 만드신 것들 넣으면 됩니다.
#     embed.add_field(
#         name='명령어 (!)',
#         value='**`안녕`**',
#         inline=False
#     )
    
#     embed.add_field(
#         name='다른 서버에 초대하려면?',
#         value='[**초대 링크**](https://초대-링크)',
#         inline=True
#     )
    
#     있다면 채널이나 그외 등등
#     embed.add_field(
#         name='궁금한 점이 있다면?',
#         value='[**독수리 채널**](https://www.youtube.com/@user-eagle10)',
#         inline=True
#     )

#     embed.set_footer(text='by (your name) (원작자 독수리)')
    
#     return embed
        
# 서버에서 봇이 나갈 때
@bot.event
async def on_guild_remove(guild:Guild):
    serverID = str(guild.id)

    def function(data:SaveData) -> None:
        if serverID in data:
            data.remove(serverID=serverID, deleteServer=True)

    forEach(datasAll, function)

# 서버에 누가 들어왔을 때
@bot.event
async def on_member_join(member:Member):
    pass

@bot.event
async def on_member_remove(member:Member):
    serverID:str = str(member.guild.id)
    userID:str = str(member.id)
    
    for data in datasUser:
        data.remove(serverID=serverID, userID=userID)
        
@bot.event
async def on_member_update(before:Member, after:Member):
    pass
        
# 그냥 대화 명령어들
@bot.command(name='안녕')
async def hello(ctx:Context):
    async with ctx.channel.typing():
        await ctx.reply('반가워요!')

@bot.command(name='수리')
async def suil(ctx:Context):
    async with ctx.channel.typing():
        await ctx.reply("`Error: Null object reference`")
    
# 기능성 명령어들
@bot.command(name='뭐해')
async def whatareyoudoing(ctx:Context):
    me:Member | discord.ClientUser = ctx.me
    activity:discord.activity.ActivityTypes | None = me.activity if isinstance(me, Member) else None
    async with ctx.channel.typing():
        if activity is not None:
            await ctx.reply(
                "아마도 아무 거나 하고 있어요\n"
                "(글쎄요, 잘 모르겠네요 `:(`)"
            )
            
        else:
            await ctx.reply(
                "할 일을 잃었어요. `:(`\n"
                "(잠깐만요, 여긴 어디죠?)"
            )


    
    










# 에러나면 여기로 감
@bot.event
async def on_command_error(ctx:Context, error:Exception):
    if isinstance(error, commands.CommandNotFound):
        pass


bot.run(TOKEN)
