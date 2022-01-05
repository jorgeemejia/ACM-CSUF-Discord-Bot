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
    await message.channel.send("Hello!!")


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


client.run(os.environ.get('TOKEN'))
