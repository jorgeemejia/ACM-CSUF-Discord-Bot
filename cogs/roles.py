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
            # token is for the id of the 'Dev Member' role
            member.guild.roles, id=int(os.environ.get('DEV')))
        algo_role = discord.utils.get(
            # token is for the id of the 'Algo Member' role
            member.guild.roles, id=int(os.environ.get('ALGO')))
        create_role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get('CREATE')))

        emoji_id = payload.emoji.id
        role_message_id = 929188792252903424  # using a random message ID to test

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
    
    # TO DO:
    # - Create an event using 'on_raw_reaction_remove'
    # - Make the event so that when a user removes their reaction from the #Get-Roles message,
    #   that relateD role is removed
    # - For example, if a user removes their :acmDev: reaction from the #Get-Roles message, then they
    #   will no longer have the 'Dev Member' role
 
    #HINTS/NOTES:
    # - Although you may think you can simply just use the code for the 'on_raw_reaction_add' event and switch out the
    #   'add_roles' function for the 'remove_roles' function, it is not that simple
    # - Note that 'on_raw_reaction_remove' doesn't allow you to retrieve the member attribute so we'll need to work around this
 
    # STEPS:
    # 1)Store the current guild in a variable using the 'fetch_guild' function
    # 2)Store the member who reacted in a variable using the 'fetch_member' function
    # 3)Now that you have access to the guild, use the 'get_role' function to store each role  
    #   into their respective Variable
    # 4)Similarly to the 'on_raw_reaction_add' event , get the message id of the #Get-Roles message and store it into a variable
    # 5)Similarly to the 'on_raw_reaction_add' event, create a check to make sure our event only responds to the #Get-Roles message
    # 6)Similarly to the 'on_raw_reaction_add' event, create if statements for each of the three roles and use the 'remove_roles' function
    #   to remove the respective role

    # @Cog.listener()
    # async def on_raw_reaction_remove(self, payload):
    #     #YOUR CODE HERE---------------------------------
        

    


def setup(bot: Bot):
    bot.add_cog(Roles(bot))
