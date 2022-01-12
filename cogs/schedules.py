from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import environ
guild_ids = [914688600828960788]

def getGuilds():
    guildList = environ.get('GUILD')
    guilds = []
    if guildList is not None:
        for guild in guildList.split(','):
            guilds.append(int(guild))
    return guilds

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", guild_ids=guild_ids)
    async def _test(self, ctx: SlashContext):
        await ctx.send(content="test")

    @cog_ext.cog_slash(name="test2", description="This command has a description", guild_ids=guild_ids)
    async def _test2(self, ctx: SlashContext):
        await ctx.send(content="test2")

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))

