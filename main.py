import discord
import os
from dotenv import load_dotenv
load_dotenv()

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
bot.load_extension("cogs.schedules")
bot.load_extension("cogs.roles")
bot.load_extension("cogs.registration")


@bot.event  #creates a bot event
async def on_ready():  #event is called using the on_ready function
  """Outputs a statement to the terminal that the bot has logged on successfully"""
  print('logged in as {0.user}'.format(bot)) #outputs a statement to the terminal


  # old code used to create the get roles channel message
  """
  channel = bot.get_channel(744067849722658827)
  msg = "Select one or more of our paths to get notifications about them!\n\n<:acmAlgo:928789715426107454>acmAlgo - Data Structure and Algorithms, Competitive Programming, Interview Prep\n<:acmDev:928789757910220862>acmDev - Software Engineering, Projects, Technical Workshops\n<:acmCreate:928789742290620437>acmCreate - Front End, Design, UI/UX\n:no_bell:Limited Notifications - Get a maximum of 1 notification every Monday that announces our plans for the week!\n:x:No Notifications at all"
  message = await channel.send(msg)
  e = bot.get_emoji(928789715426107454)
  print(type(e))
  await message.add_reaction(e)
  e = bot.get_emoji(928789757910220862)
  await message.add_reaction(e)
  e = bot.get_emoji(928789742290620437)
  await message.add_reaction(e)
  await message.add_reaction('\U0001F515')
  await message.add_reaction('\u274C')
  """



bot.run(os.environ.get('TOKEN'))
