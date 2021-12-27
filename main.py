import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)



@client.event  #creates a client event
async def on_ready():  #event is called using the on_ready function
  """Outputs a statement to the terminal that the bot has logged on successfully"""
  print('logged in as {0.user}'.format(client)) #outputs a statement to the terminal


@client.event
async def on_message(message):
  """Whenever a user says 'Hi', the bot will respond with 'Hello'"""
  if message.content == "Hi":
    await message.channel.send("Hello")


client.run(os.environ.get('TOKEN'))
