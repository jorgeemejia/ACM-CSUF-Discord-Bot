import discord
import os
from dotenv import load_dotenv
load_dotenv()

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.load_extension("cogs.schedules")
bot.load_extension("cogs.roles")

slash = SlashCommand(bot, sync_commands=True)

@bot.event  #creates a bot event
async def on_ready():  #event is called using the on_ready function
  """Outputs a statement to the terminal that the bot has logged on successfully"""
  print('logged in as {0.user}'.format(bot)) #outputs a statement to the terminal

bot.run(os.environ.get('TOKEN'))