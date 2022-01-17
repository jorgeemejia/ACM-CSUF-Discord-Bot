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
