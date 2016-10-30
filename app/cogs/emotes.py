from discord.ext.commands import Bot

EMOTES = {
    'lenny': '( ͡° ͜ʖ ͡°)',
    'giff': '༼ つ ◕_◕ ༽つ',
    'disapproval': 'ಠ_ಠ',
    'donger': 'ヽ༼ຈل͜ຈ༽ﾉ',
}

CLASS_TEMPLATE = '''
from discord.ext import commands
class Emotes:
    def __init__(self, bot):
        self.bot = bot
''' + '{}' * len(EMOTES)

COMMAND_TEMPLATE = '''
    @commands.command(help='{emote}')
    async def {name}(self):
        await self.bot.say('{emote}')
'''


def generate_class():
    """I'm so sorry"""
    command_strings = []
    for name, emote in EMOTES.items():
        command = COMMAND_TEMPLATE.format(name=name, emote=emote)
        command_strings.append(command)

    class_string = CLASS_TEMPLATE.format(*command_strings)
    # print(class_string)
    exec(class_string, globals())


def setup(bot: Bot):
    generate_class()
    bot.add_cog(Emotes(bot))
