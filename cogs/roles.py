from discord.ext.commands import Bot, Cog
import os
import discord
from discord.ext.commands.converter import TextChannelConverter
from dotenv import load_dotenv
load_dotenv()


class Roles(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.content == "Hi":
            await message.channel.send("Hello")
    
    @Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, id=int(os.environ.get('NEWCOMER'))) #NEWCOMER is the id of the NewComer role in my server
        await member.add_roles(role)


    @Cog.listener()
    async def on_raw_reaction_add(self, payload):

        member = payload.member

        dev_role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get('DEV')))
        algo_role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get('ALGO')))
        create_role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get('CREATE')))

        emoji_id = payload.emoji.id
        role_message_id = 931018904866799616  # using a random message ID to test

        if payload.message_id == role_message_id:
            # token is for the dev emoji ID
            if emoji_id == int(os.environ.get('DEVEMOJI')):
                await member.add_roles(dev_role)
            # token is for the algo emoji ID
            elif emoji_id == int(os.environ.get('ALGOEMOJI')):
                await member.add_roles(algo_role)
            # token is for the create emoji ID
            elif emoji_id == int(os.environ.get('CREATEEMOJI')):
                await member.add_roles(create_role)

    


def setup(bot: Bot):
    bot.add_cog(Roles(bot))
