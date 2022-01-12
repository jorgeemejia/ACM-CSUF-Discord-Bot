from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from sys import path
path.append('../')
from helpers import getGuilds

guild_ids = getGuilds()

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @cog_ext.cog_slash(name="test", guild_ids=guild_ids)
    async def _test(self, ctx: SlashContext):
        await ctx.send(content="test")

    @cog_ext.cog_slash(name="test2", description="This command has a description", guild_ids=guild_ids)
    async def _test2(self, ctx: SlashContext):
        await ctx.send(content="test2")

    # for aaron to do:
        # code for subcommands
        # code for json example
        # embed help

    # two json files, classes.json, students.json

    # /schedule 
        # open the students.json file
        # return the students classes
        # display button asking to share to the channel

    # /schedule add
        # open both json files
        # validate the input
        # add the class to the person
        # add the person to the class
        # give them the role/permissions
        
    # /schedule remove
        # open both json files
        # check if the student is in that class
        # remove the class from the student
        # remove the student from the class
        # update their roles/permissions
    
    """
    Create your own command that allows a user to run /schedule, and it will return a link to the google form ("https://docs.google.com/forms/d/1sz-YZ3QkpTkVMFYlX8Mt0k1jhJrSY1BPzXMMUVdCEXs/edit")

    Create a description for the command as well.
    """

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))

