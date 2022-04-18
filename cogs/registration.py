from discord import utils
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
from os import environ
from dotenv import load_dotenv
load_dotenv()
from helpers import getGuilds, isCsufEmail, sendError, sendMessage
from random import randint

import smtplib
from email.mime.text import MIMEText
import base64

SHOW_MESSAGES = False
SHOW_ERRORS = False

from datetime import datetime
from email.mime.text import MIMEText
import base64

HIDE_MESSAGES = True
HIDE_ERRORS = True


import logging
logging.basicConfig(filename='logs/registration.log',format='[%(levelname)s] %(asctime)s %(message)s', level=logging.DEBUG)

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
            await sendError(ctx, str(e), hidden=HIDE_ERRORS)
        return False

guild_ids = getGuilds()

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

def send_email(email, code):
    usr = environ.get('SENDER_EMAIL')
    pwd = environ.get('SENDER_PASSWORD')
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(usr, pwd) 

    message = MIMEText("Verification code: <h1>{}</h1> Use <code>/verify</code> in the discord server to complete your registration.<br> If you did not authorize this email, please ignore.".format(code), 'html', 'UTF-8')
    message['to'] = email
    message['from'] = environ.get('SENDER_EMAIL')
    message['subject'] = "acmCSUF discord verification"

    session.sendmail(usr, email, message.as_string())
    session.quit()

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    """

        /register <csuf_email>

    """
    @cog_ext.cog_slash(name="register", description="register using your CSUF email to get access to the server!", guild_ids=guild_ids, default_permission=True)
    async def _register(self, ctx: SlashContext, csuf_email: str, first_name: str, last_name: str, pronouns: str, show_pronouns: bool = True):
        csuf_email = csuf_email.lower()

        # Validate the email is a csuf email
        if not isCsufEmail(csuf_email):
            return await sendError(ctx, "Invalid CSUF email")

        # Check if the user's discord account is already registered
        q = 'SELECT COUNT(*) FROM MEMBER WHERE discordId = %s;'
        d = (ctx.author.id,)
        result = await query(q, d, ctx) 
        if result == False: return
        if (result[0][0] != 0):
            return await sendError(ctx, "User already registered")

        # check if the user's email already exists
        q = 'SELECT COUNT(*) FROM MEMBER WHERE email = %s;'
        d = (csuf_email,)
        result = await query(q, d, ctx) 
        if result == False: return
        if (result[0][0] != 0):
            return await sendError(ctx, "This email is already registered on another discord account. Contact a board member for help")

        # generate verification code
        code = str(randint(0, 999999)).zfill(6) # padded 6 digit num
        
        # remove old/duplicate verification codes
        q = 'DELETE FROM VERIFICATION WHERE createdAt <= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE OR email = %s;'
        d = (csuf_email,)
        result = await query(q, d, ctx)
        if result == False: return

        # parse user pronouns
        if show_pronouns:
            pronouns = "(" + pronouns.replace(" ", "").replace("(", "").replace(")", "") + ")"
        else:
            pronouns = None

        # generate the verification code, and insert user info into the table
        q = 'INSERT INTO VERIFICATION (discordId, email, firstName, lastName, pronouns, code, createdAt) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)'
        d = (ctx.author.id, csuf_email, first_name, last_name, pronouns, code)
        result = await query(q, d, ctx)
        if result == False: return

        try:
            send_email(csuf_email, code)

        except Exception as e:
            logging.error(str(e))
            await sendError(ctx, "Unable to send verification email")


        await sendMessage(ctx, "A verification code has been sent to your email. Please run the /verify command with the code provided.", hidden=HIDE_MESSAGES)


    """

     /verify <verification_code>

    """
    @cog_ext.cog_slash(name="verify", description="Verify your email after running the /register command", guild_ids=guild_ids, default_permission=True)
    async def _verify(self, ctx: SlashContext, verification_code: str):

        # Check for verification codes 5 minutes or less, with the discordId of the current user, and return the email
        q = 'SELECT email, firstName, lastName, pronouns FROM VERIFICATION WHERE createdAt >= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE AND discordId = %s AND code = %s;'
        d = (ctx.author.id, verification_code)
        result = await query(q, d, ctx)
        if result == False: return
        if (result == []):
            return await sendError(ctx, "The code you entered was incorrect or was more than 5 minutes old and has expired.")
        email = result[0][0]
        firstName = result[0][1]
        lastName = result[0][2]
        pronouns = result[0][3]

        # Insert a new row into the database 
        q = 'INSERT INTO MEMBER (email, discordId, firstName, lastName, pronouns) VALUES (%s, %s, %s, %s, %s)'
        d = (email, ctx.author.id, firstName, lastName, pronouns)
        result = await query(q, d, ctx)
        if result == False: return

        # form name and add pronouns 
        name = "{} {}".format(firstName, lastName)
        if pronouns:
            name += " {}".format(pronouns)

        # Change the user's nickname
        try:
            await ctx.author.edit(nick=name)
        except Exception as e:
            logging.error(str(e))
            await sendError(ctx, "Cannot change name, I don't have more permissions than you!")

        # Find the verified role and add it to the user
        try:
            verified_email_role = utils.get(ctx.guild.roles,name="Verified Email")
            await ctx.author.add_roles(verified_email_role)
        except Exception as e:
            logging.error(str(e))
            return await sendError(ctx, "Failed to add role")

        roles_channel = environ.get('ROLE_CHANNEL_ID')

        await sendMessage(ctx, f"Successfully verified your email! Last step, go to <#{roles_channel}> and select a role to complete your registration.", hidden=HIDE_MESSAGES)


def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
