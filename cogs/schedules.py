from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from os import path
from os import environ
import json
from helpers import getGuilds, sendError, sendMessage, standardTime, generatePermissions
import discord
from datetime import datetime
import re

guild_ids = getGuilds()
permissions = generatePermissions()

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

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    """

    /schedule view

    """

    @cog_ext.cog_subcommand(base="schedule", name="view", description="View your schedule", guild_ids=guild_ids, base_default_permission=False, base_permissions=permissions)
    async def _schedule_view(self, ctx: SlashContext, semester: str = getEnrollmentSemester()):

        # Validate the semester input
        semester = semester.upper()
        if (semester != "FALL" and semester != "SPRING"):
            return await sendError(ctx, "Invalid semester, please choose Fall or Spring.")

        # Get all of the students classes for the semester 
        q = 'SELECT subject, number, section, startTime, endTime FROM CLASS INNER JOIN DISCORDSCHEDULE ON (DISCORDSCHEDULE.classId = CLASS.id) WHERE discordId = %s AND year = %s AND semester = %s;'
        d = (ctx.author.id, getYearFromSemester(semester), semester)
        result = await query(q, d, ctx)
        if result is None: return

        # if there are no classes
        if not result:
            await sendMessage(ctx, "Your {} schedule is empty, use the `/schedule add` command to add your classes!".format(semester))
            return
        
        # create embeded message
        embed=discord.Embed(title="Hello " + ctx.author.display_name + "!", description="Here are your classes:", color=0xFF5733)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        # add fields and format times to embeded message
        for c in result:
            embed.add_field(name='{} {}-{}'.format(c[0], c[1], c[2]), value='{} - {}'.format(standardTime(c[3]), standardTime(c[4])), inline=False)
        await ctx.send(embed=embed)

    """

    /schedule add

    """

    @cog_ext.cog_subcommand(base="schedule", name="add", description="Add a class to your schedule. Must include the section!", guild_ids=guild_ids, base_default_permission=False, base_permissions=permissions)
    async def _schedule_add(self, ctx: SlashContext, course: str, semester: str = getEnrollmentSemester()):

        # Validate the semester input
        semester = semester.upper()
        if (semester != "FALL" and semester != "SPRING"):
            return await sendError(ctx, "Invalid semester, please choose Fall or Spring.")
        
        # Verify that the course is a valid course.
        reg = re.search(r".*[A-Za-z]{4}\s*[0-9]{3}[A-Za-z]?\s*-\s*[0-9]{1,2}.*", course)
        if not (reg):
            return await sendError(ctx, "Invalid class. Make sure you follow the correct format. Example: CPSC 131-05")

        # remove all whitespace
        components = "".join(course.split()).split('-')
        subject = components[0][0:4]
        number = components[0][4:]
        section = int(components[1])

        # Find the classId
        q = 'SELECT id FROM `CLASS` WHERE subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;'
        d = (subject, number, section, getEnrollmentSemester())
        result = await query(q, d, ctx)
        if result is None: return
        if not result:
            return await sendError(ctx, "Class not found. Ask for help if you believe this is a mistake")
        classId = result[0][0]

        # check for duplicates
        q = 'SELECT COUNT(*) FROM DISCORDSCHEDULE WHERE discordId = %s AND classId = %s;'
        d = (ctx.author.id, classId)
        result = await query(q, d, ctx)
        if result is None: return
        if result[0][0] > 0:
            return await sendError(ctx, "You've already added this class. Use `/schedule view` to see your current schedule")

        # Add the class to the student's schedule
        q = 'INSERT INTO DISCORDSCHEDULE (discordId, classId) VALUES (%s, %s)'
        d = (ctx.author.id, classId)
        result = await query(q, d, ctx)
        if result is None: return

        await sendMessage(ctx, "Successfully added".format(course))

        # Check if a student is the first one to join a course
        q = 'SELECT A.subject, A.number, A.discordChannel FROM COURSECHANNEL AS A, (SELECT subject, number FROM CLASS INNER JOIN DISCORDSCHEDULE ON (DISCORDSCHEDULE.classId = CLASS.id) WHERE classId = %s) AS B WHERE A.subject = B.subject AND A.number = B.number;'
        d = (classId,)
        result = await query(q, d, ctx)
        if result is None: return

        # if this user is the first one to add the class
        if result == []:
            guild = ctx.guild
            member = ctx.author
            overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True),
                    }
            cat = discord.utils.get(guild.categories, name="classes")
            channel_name = f"{subject} {number}"
            channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=cat)
            message = await channel.send("Welcome to the private text channel! Here you can interact with students who are taking the same course!")
            await message.pin()

            q = 'INSERT INTO COURSECHANNEL (subject, number, discordChannel) VALUES (%s, %s, %s);'
            d = (subject, number, channel.id)
            result = await query(q, d, ctx)
            if result is None: return

            await sendMessage(ctx, f"You can now access <#{channel.id}> Here you can interact with students who are taking the same course! It seems that you are alone in this channel, but don't worry fellow students will arrive when they add the same course to their schedule!", hidden=True)
        else:
            discordChannel = result[0][2]
            overwrites = ctx.channel.overwrites_for(ctx.author)
            overwrites.send_messages, overwrites.read_messages = True, True
            await ctx.channel.set_permissions(ctx.author, overwrite=overwrites)
            await sendMessage(channel, f"You can now access <#{discordChannel}> Here you can interact with students who are taking the same course!", hidden=True)





    """

    /schedule remove

    """

    @cog_ext.cog_subcommand(base="schedule", name="remove", description="Remove a class from your schedule. Must include the section!", guild_ids=guild_ids, base_default_permission=False, base_permissions=permissions)
    async def _schedule_remove(self, ctx: SlashContext, course: str, semester: str = getEnrollmentSemester()):

        # Validate the semester input
        semester = semester.upper()
        if (semester != "FALL" and semester != "SPRING"):
            return await sendError(ctx, "Invalid semester, please choose Fall or Spring.")

        # Verify that the course is a valid course.
        reg = re.search(r".*[A-Za-z]{4}\s*[0-9]{3}[A-Za-z]?\s*-\s*[0-9]{1,2}.*", course)
        if not (reg):
            return await sendError(ctx, "Invalid class. Make sure you follow the correct format. Example: CPSC 131-05")

        # remove all whitespace
        components = "".join(course.split()).split('-')
        subject = components[0][0:4]
        number = components[0][4:]
        section = int(components[1])

        # Find the classId
        q = 'SELECT id FROM `CLASS` WHERE subject = %s AND number = %s AND section = %s AND `year` = year(curdate()) AND semester = %s;'
        d = (subject, number, section, getEnrollmentSemester())
        result = await query(q, d, ctx)
        if result is None: return
        if not result:
            return await sendError(ctx, "Class not found. Ask for help if you believe this is a mistake")
        classId = result[0][0]

        # check for duplicates
        q = 'SELECT COUNT(*) FROM DISCORDSCHEDULE WHERE discordId = %s AND classId = %s;'
        d = (ctx.author.id, classId)
        result = await query(q, d, ctx)
        if result is None: return
        if result[0][0] < 1:
            return await sendError(ctx, "You are not enrolled in the course {}".format(course))

        # remove the class from the students schedule
        q = 'DELETE FROM DISCORDSCHEDULE WHERE discordId = %s AND classId = %s;'
        d = (ctx.author.id, classId)
        result = await query(q, d, ctx)
        if result is None: return

        await sendMessage(ctx, "Successfully removed")

        # check the number of students 
        q = 'SELECT COUNT(*) FROM DISCORDSCHEDULE INNER JOIN CLASS ON (DISCORDSCHEDULE.classId = CLASS.id) WHERE subject = %s AND number = %s;'
        d = (subject, number)
        result = await query(q, d, ctx)
        if result is None: return

        num_students = result[0][0]

        # get the channelId
        q = 'SELECT discordChannel FROM COURSECHANNEL WHERE subject = %s AND number = %s;'
        d = (subject, number)
        result = await query(q, d, ctx)
        if result is None: return

        channel_id = result[0][0]
        print(num_students)

        # if there are no more students in the channel, delete the channel
        if num_students == 0:
            q = 'DELETE FROM COURSECHANNEL WHERE subject = %s and number = %s;'
            d = (subject, number)
            result = await query(q, d, ctx)
            if result is None: return

            print(channel_id)

            channel = self.bot.get_channel(int(channel_id))
            await channel.delete()

        # otherwise, remove their permissions
        else:
            discordChannel = result[0][1]
            overwrites = ctx.channel.overwrites_for(ctx.author)
            overwrites.send_messages, overwrites.read_messages = False, False
            await ctx.channel.set_permissions(ctx.author, overwrite=overwrites)



def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
