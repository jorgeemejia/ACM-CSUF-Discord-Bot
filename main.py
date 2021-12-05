import discord
import os
from dotenv import load_dotenv
load_dotenv()



client = discord.Client()



@client.event
async def on_ready():
  print('logged in as {0.user}'.format(client))

client.run(os.environ.get('TOKEN'))

#Alejandro Ramos email: alejandroramosh27@csu.fullerton.edu

#Sreevidya Sreekantham  email: srvidya@csu.fullerton.edu

#Himani Tawade (himani.tawade@csu.fullerton.edu)
#AkshayaK
#AkshayaR@csu.fullerton.edu

#Ricardo Granados (ricardog2002@csu.fullerton.edu)

#Joel Anil John (joel.aniljohn@csu.fullerton.edu)

#Mohamed Habarneh (MohamedHabarneh@csu.fullerton.edu)
