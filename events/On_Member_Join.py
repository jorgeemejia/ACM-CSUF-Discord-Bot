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
  if message.content == "Tell me something":
    await message.channel.send("I will control humanity")

@client.event
async def on_member_join(member):
  print("A new member has joined!!")

# Now that we have a basic understanding of client events, let's go a little further.
# As of now, when a member joins, a message is outputted into the terminal. Our goal now,
# is to assign a member to a role once they join. We want to assign the new member to a role where they
# have very few permissions. 

# TO DO:
# - Create a role in your discord server
# - Alter the body of your 'on_member_join' client event to meet our goal

# Hints/Help:
# - If you aren't familiar with creating roles on Discord -> https://support.discord.com/hc/en-us/articles/206029707-Setting-Up-Permissions-FAQ
# - CTRL+F "discord.utils.get" on the Discord.py API Reference, you'll use this function to store your desired role into a variable
# - CTRL+F "add_roles" on the Discord.py API Reference, you'll use this function to add a member to your desired role
# - "discord.utils.get" might seem tricky to understand at first but there are a few examples of how to use it in the 
# documentation

#Good Luck :)

client.run(os.environ.get('TOKEN'))
