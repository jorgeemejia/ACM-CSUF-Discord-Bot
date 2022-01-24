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

async def sendMessage(ctx, message, hidden=False, pinned=False, channel=None):
    embed=Embed(description=message, color=0x00ff00)
    message = await ctx.send(embed=embed, hidden=hidden)
    if (pinned and not hidden):
        await message.pin()

def standardTime(time):
    if time.days > 0:
        return "12:00am"
    time = str(time)
    m = "am"
    components = time.split(':')
    hours = int(components[0])
    minutes = str(components[1])
    if (hours >= 12): m = "pm"
    if (hours >= 13): hours -= 12
    return "{}:{}{}".format(hours, minutes, m)

from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

def generatePermissions():
    perms = {}
    guild_ids = getGuilds()
    verified_role = environ.get('VERIFIED_ROLE_ID')
    perms[guild_ids[0]] = [create_permission(verified_role, SlashCommandPermissionType.ROLE, True)]
    return perms


