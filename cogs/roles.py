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
    async def on_raw_reaction_add(self, payload):
        role_message_id = int(os.environ.get('GET_ROLE_MESSAGE'))
        if payload.message_id == role_message_id:
            
            member = payload.member
            dev_role = discord.utils.get(member.guild.roles, name='Dev Member')
            algo_role = discord.utils.get(member.guild.roles, name='Algo Member')
            create_role = discord.utils.get(member.guild.roles, name='Create Member')

            emoji_name = payload.emoji.name
            if emoji_name == 'acmDev':
                await member.add_roles(dev_role)
            elif emoji_name == 'acmAlgo':
                await member.add_roles(algo_role)
            elif emoji_name == 'acmCreate':
                await member.add_roles(create_role)
            else: 
                return
    

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        role_message_id = int(os.environ.get('GET_ROLE_MESSAGE'))
        if payload.message_id == role_message_id:
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)

            dev_role = discord.utils.get(guild.roles, name='Dev Member')
            create_role = discord.utils.get(guild.roles, name='Create Member')
            algo_role = discord.utils.get(guild.roles, name='Algo Member')

            if payload.emoji.name == 'acmDev': 
                await member.remove_roles(dev_role)
            elif payload.emoji.name == 'acmCreate':
                await member.remove_roles(create_role)
            elif payload.emoji.name == 'acmAlgo':
                await member.remove_roles(algo_role)
            else: 
                return



def setup(bot: Bot):
    bot.add_cog(Roles(bot))
