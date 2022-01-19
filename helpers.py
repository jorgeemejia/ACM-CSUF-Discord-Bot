from os import environ

def getGuilds():
    guildList = environ.get('GUILD')
    guilds = []
    if guildList is not None:
        for guild in guildList.split(','):
            guilds.append(int(guild))
    return guilds


import re

def isCsufEmail(email):
    return bool(re.search(r".*@(.+\.)?fullerton.edu$", email))

from discord import Embed
from datetime import datetime

async def sendError(ctx, message, hidden=False):
    embed=Embed(title="ERROR", description=message, color=0xff0000)
    embed.add_field(name="Help", value="If needed, use <#{}> to get assistance".format(environ.get('HELP_CHANNEL_ID')), inline=False)
    embed.set_footer(text=str(datetime.now()))
    await ctx.send(embed=embed, hidden=hidden)

async def sendMessage(ctx, message, hidden=False):
    embed=Embed(description=message, color=0x00ff00)
    await ctx.send(embed=embed, hidden=hidden)

def standardTime(time):
    m = "am"
    components = time.split(':')
    hours = int(components[0])
    minutes = int(components[1])
    if (hours >= 12) m = "pm"
    if (hours >= 13) hours -= 12
    return "{}:{}{}".format(hours, minutes, m)

