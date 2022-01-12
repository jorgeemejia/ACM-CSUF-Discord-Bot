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

    def fetchGoogleFormResults():
        # Fetch the google form results every 15s
        # process the new results, and pass them to the confirmUser function 
        pass

    def confirmUser(user, classes):
        # Find the user by discord tag
        # DM them the classes, check that this is the correct user, and the correct classes
        # Display the message using discord's embedded messages
        # Have a user click a button to confirm everything is correct
        pass


    @cog_ext.cog_slash(name="test", guild_ids=guild_ids)
    async def _test(self, ctx: SlashContext):
        await ctx.send(content="test")

    @cog_ext.cog_slash(name="test2", description="This command has a description", guild_ids=guild_ids)
    async def _test2(self, ctx: SlashContext):
        await ctx.send(content="test2")

    @cog_ext.cog_slash(name="schedule", description="This command has a description", guild_ids=guild_ids)
    async def schedule(self, ctx: SlashContext):
        await ctx.send(content="https://docs.google.com/forms/d/1sz-YZ3QkpTkVMFYlX8Mt0k1jhJrSY1BPzXMMUVdCEXs/edit")

    
    """
    Create your own command that allows a user to run /schedule, and it will return a link to the google form ("https://docs.google.com/forms/d/1sz-YZ3QkpTkVMFYlX8Mt0k1jhJrSY1BPzXMMUVdCEXs/edit")

    Create a description for the command as well.
    """

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
