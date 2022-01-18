from discord import utils
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
from os import environ
from dotenv import load_dotenv
load_dotenv()
from helpers import getGuilds, isCsufEmail, sendError, sendMessage
from random import randint
from email.mime.text import MIMEText
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import logging
logging.basicConfig(filename='logs/registration.log',format='[%(levelname)s] %(asctime)s %(message)s', level=logging.DEBUG)

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
        return False


def authenticate_gmail():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    SCOPES = ['https://mail.google.com/']
    if path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8888)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Return the gmail service
        return build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        print(f'Cannot connect to gmail API: {error}')


class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.gmailService = authenticate_gmail()

    """

        /register <csuf_email>

    """
    @cog_ext.cog_slash(name="register", description="register using your CSUF email to get access to the server!", guild_ids=guild_ids)
    async def _register(self, ctx: SlashContext, csuf_email: str, first_name: str, last_name: str, pronouns: str, show_pronouns: bool = True):

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
        
        # create the email message
        message = MIMEText("Your verification code is {}. Use /verify in discord server to complete your registration.".format(code))
        message['to'] = csuf_email
        message['from'] = environ.get('SENDER_EMAIL')
        message['subject'] = "acmCSUF discord verification"
        body = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

        # send the email
        try:
            message = (self.gmailService.users().messages().send(userId=environ.get('SENDER_EMAIL'), body=body).execute())
        except Exception as e:
            logging.error(str(e))
            await sendError(ctx, "Unable to send verification email")


        await sendMessage(ctx, "A verification code has been sent to your email. Please run the /verify command with the code provided. (Pssst... its {})".format(code))


    """

     /verify <verification_code>

    """
    @cog_ext.cog_slash(name="verify", description="Verify your email after running the /register command", guild_ids=guild_ids)
    async def _verify(self, ctx: SlashContext, verification_code: str):

        # Check for verification codes 5 minutes or less, with the discordId of the current user, and return the email
        q = 'SELECT COUNT(*), email, firstName, lastName, pronouns FROM VERIFICATION WHERE createdAt >= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE AND discordId = %s AND code = %s;'
        d = (ctx.author.id, verification_code)
        result = await query(q, d, ctx)
        if result == False: return
        if (result[0][0] < 1):
            return await sendError(ctx, "The code you entered was incorrect or has expired")
        email = result[0][1]
        firstName = result[0][2]
        lastName = result[0][3]
        pronouns = result[0][4]

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
            verified_role = utils.get(ctx.guild.roles,name="Verified")
            await ctx.author.add_roles(verified_role)
        except Exception as e:
            logging.error(str(e))
            return await sendError(ctx, "Failed to add role")

        await sendMessage(ctx, "Successfully Registered!")


def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
