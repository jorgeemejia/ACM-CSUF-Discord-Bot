from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
from os import environ
import json
from helpers import getGuilds
import discord
from datetime import datetime

guild_ids = getGuilds()

classes_path = path.relpath("data/classes.json")
students_path = path.relpath("data/students.json")

import mysql.connector
mysql_options = {
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASS'),
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'autocommit': True
        }
db = mysql.connector.connect(**mysql_options)
cursor = db.cursor()

def getEnrollmentSemester():
    month = datetime.now().month 
    return 'SPRING' if month > 9 or month < 2 else 'FALL'

def getYearFromSemester(semester):
    now = datetime.now()
    if (semester == "FALL"):
        return now.year + 1
    else: 
        return now.year

def addClass(discordId, subject, number, section, semester):
    try:
        cursor.execute('SELECT id from `CLASS` WHERE discordId = %s AND subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;', (discordId, subject, number, section, getEnrollmentSemester()))
        classId = cursor.fetchone()[0]
        cursor.execute('INSERT INTO DISCORDSCHEDULE (discordId, classId) VALUES (%s, %s)', (discordId, classId))
    except Exception as e:
        raise

def removeClass(discordId, subject, number, section, semester):
    try:
        cursor.execute('SELECT id from `CLASS` WHERE discordId = %s AND subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;', (discordId, subject, number, section, getEnrollmentSemester()))
        classId = cursor.fetchone()[0]
        cursor.execute('DELETE FROM DISCORDSCHEDULE WHERE classId = %s AND discordId = %s', (classId, discordId))
    except Exception as e:
        raise

def getClasses(discordId, semester):
    try:
        cursor.execute('SELECT * FROM DISCORDSCHEDULE WHERE discordId = %s AND `year` = %s AND semester = %s;', (discordId, getYearFromSemester(semester), semester))
    except Exception as e:
        raise
    results = cursor.fetchall()
    return results

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="schedule", name="view", description="View your schedule", guild_ids=guild_ids)
    async def _schedule_view(self, ctx: SlashContext):
        embed=discord.Embed(title="Hello " + ctx.author.display_name + "!", 
    description="Here are your classes:", 
    color=0xFF5733)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        classes = students[ctx.author.display_name]
        for class_name in classes:
            idx = class_name.index("-")
            class_session = class_name[idx+1:]
            embed.add_field(name=class_name[:idx], value="Session: " + class_session, inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="schedule", name="add", description="Add a class to your schedule", guild_ids=guild_ids)
    async def _schedule_add(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule add")

    @cog_ext.cog_subcommand(base="schedule", name="remove", description="Remove a class from your schedule", guild_ids=guild_ids)
    async def _schedule_remove(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule remove")

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
