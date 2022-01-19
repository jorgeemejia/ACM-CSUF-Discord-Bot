from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
from os import environ
import json
from helpers import getGuilds, sendError, sendMessage
import discord
from datetime import datetime

guild_ids = getGuilds()

import logging
logging.basicConfig(filename='logs/schedules.log',format='[%(levelname)s] %(asctime)s %(message)s', level=logging.DEBUG)

async def query(q, d, ctx=None):
    try:
        logging.info(q)
        cursor.execute(q, d)
        result = cursor.fetchall()
        logging.info(str(result))
        return result
    except Exception as e:
        print(str(e))
        logging.error(str(e))
        if (ctx):
            await sendError(ctx, str(e))
        return None

import mysql.connector
mysqlOptions = {
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASS'),
        'host': environ.get('DB_HOST'),
        'database': environ.get('DB_NAME'),
        'autocommit': True
        }
db = mysql.connector.connect(**mysqlOptions)
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
"""
def addClass(discordId, subject, number, section, semester):
    # Find the classId
    q = 'SELECT id from `CLASS` WHERE discordId = %s AND subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;'
    d = (discordId, subject, number, section, getEnrollmentSemester())
    result = await query(q, d, ctx)
    if result is None: return
    classId = result[0][0]

    # Add the class to the student's schedule
    q = 'INSERT INTO DISCORDSCHEDULE (discordId, classId) VALUES (%s, %s)'
    d = (discordId, classId)
    result = await query(q, d, ctx)
    if result is None: return

def removeClass(discordId, subject, number, section, semester):
    # find the classId
    q = 'SELECT id from `CLASS` WHERE discordId = %s AND subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;'
    d = (discordId, subject, number, section, getEnrollmentSemester())
    result = await query(q, d, ctx)
    if result is None: return
    classId = result[0][0]

    # delete the class from the student's schedule
    q = 'DELETE FROM DISCORDSCHEDULE WHERE classId = %s AND discordId = %s'
    d = (classId, discordId)
    result = await query(q, d, ctx)
    if result is None: return
"""

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="schedule", name="view", description="View your schedule", guild_ids=guild_ids)
    async def _schedule_view(self, ctx: SlashContext, semester: str = getEnrollmentSemester()):

        # Get all of the students classes for the semester 
        q = 'SELECT subject, number, section, startTime, endTime FROM CLASS INNER JOIN DISCORDSCHEDULE ON (DISCORDSCHEDULE.classId = CLASS.id) WHERE discordId = %s AND year = %s AND semester = %s;'
        d = (ctx.author.id, getYearFromSemester(semester), semester)
        result = await query(q, d, ctx)
        print(result)
        if result is None: return

        # if there are no classes
        if not result:
            await sendMessage(ctx, "Your {} schedule is empty, use the `/schedule add` command to add your classes!".format(semester))
            return

        embed=discord.Embed(title="Hello " + ctx.author.display_name + "!", description="Here are your classes:", color=0xFF5733)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        for c in result:
            embed.add_field(name='{} {}-{}'.format(c[0], c[1], c[2]), value='{} - {}'.format(c[3], c[4]), inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="schedule", name="add", description="Add a class to your schedule", guild_ids=guild_ids)
    async def _schedule_add(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule add")

    @cog_ext.cog_subcommand(base="schedule", name="remove", description="Remove a class from your schedule", guild_ids=guild_ids)
    async def _schedule_remove(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule remove")

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
