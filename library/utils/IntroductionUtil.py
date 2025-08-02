from library.preimport import *

class IntroductionUtil():
    @staticmethod
    def getEagleIntroduction(bot:Bot) -> Embed:
        NOW:datetime = datetime.now()
        if bot.user == None:
            return ErrorUtil.getErrorEmbed(ErrorEmbedType.BOT_LOGOUTED, NOW)
        
        embed = Embed(
            title=f'`{bot.user.display_name}`의 소개문',
            color=Color.from_rgb(139, 69, 19),
            timestamp=NOW
        )
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.add_field(name='개발자', value='[수리](https://www.youtube.com/@user-eagle10)', inline=False)
        embed.add_field(name='개발 언어', value='Python (Discord.py 2.4.0)', inline=False)
        embed.add_field(name='마크 2인 이유', value='세대 교체, 그 외 기타 등등의 이유', inline=False)
        embed.add_field(name='기능', value='여러 가지 명령어들과 편의성을 올려주는 기능들 사용 가능', inline=False)
        embed.add_field(name='취미', value='죽은 원본 독수리봇 [추모하기](https://youtu.be/9oayxL1J2nY)', inline=False)
        
        return embed