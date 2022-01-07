from discord.ext.commands import Bot, Cog
from os import environ

class Roles(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


#MEMBER_JOIN :

#The first step of creating the 'member_join' functionality is figuring out a way to see when someone joins the discord server.
#So that's what we'll be figuring out first.

#TO DO:
# Looking at the structure of the client events above, create another client event that is called when a member joins the discord server
# HINT: ctrl+f "on_member_join" in the discord.py API Reference https://discordpy.readthedocs.io/en/stable/api.html

# Make it so whenever someone joins the discord server, a statement is outputted in the terminal.
# (You can simulate someone joining your server by inviting another bot to your server.
# There are tons of sites with tons of bots, just choose one and have them join)
# Here is a link to a site that let's you invite bots to your server: https://top.gg/

    @Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @Cog.listener()
    async def on_message(self, message):
        if message.content == "Hi":
            await message.channel.send("Hello")


def setup(bot: Bot):
    bot.add_cog(Roles(bot))
