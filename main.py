import discord
import os
from dotenv import load_dotenv
load_dotenv()



client = discord.Client()



@client.event
async def on_ready():
  """Outputs a statement to the terminal that the bot has logged on successfully"""
  print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  """Whenever a user says 'Hi', the bot will respond with 'Hello'"""
  if message.content == "Hi":
    await message.channel.send("Hello")

client.run(os.environ.get('TOKEN'))