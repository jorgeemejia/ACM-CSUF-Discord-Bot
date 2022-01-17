from discord import Embed, utils
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
from os import environ
from dotenv import load_dotenv
load_dotenv()
from helpers import getGuilds, isCsufEmail
from random import randint

guild_ids = getGuilds()

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



class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    """""""""""""""""""""""""""""""

        /register <csuf_email>

    """""""""""""""""""""""""""""""
    @cog_ext.cog_slash(name="register", description="register using your CSUF email to get access to the server!", guild_ids=guild_ids)
    async def _register(self, ctx: SlashContext, csuf_email: str):

        # Validate the email is a csuf email
        if not isCsufEmail(csuf_email):
            return await ctx.send("Invalid email, or not a CSUF email")

        # Check if the user's discord account is already registered
        try:
            cursor.execute('SELECT COUNT(*) FROM MEMBER WHERE discordId = %s;', (ctx.author.id,)) 
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))
        if (cursor.fetchall()[0][0] != 0):
            return await ctx.send("User already registered")

        # check if the user's email already exists
        try:
            cursor.execute('SELECT COUNT(*) FROM MEMBER WHERE email = %s;', (csuf_email,)) 
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))
        if (cursor.fetchall()[0][0] != 0):
            return await ctx.send("This email is already registered. If you would like to switch the email to the current discord account, please contact a board member.")

        # remove old/duplicate verification codes
        code = str(randint(0, 999999)).zfill(6) # padded 6 digit num

        try:
            cursor.execute("DELETE FROM VERIFICATION WHERE createdAt <= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE OR email = %s;", (csuf_email,))
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))

        # generate the verification code
        try:
            cursor.execute('INSERT INTO VERIFICATION (discordId, email, code, createdAt) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)', (ctx.author.id, csuf_email, code))
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))

        await ctx.send(content="A verification code has been sent to your email. Please run the /verify command with the code provided. (Pssst... its {})".format(code))


    """""""""""""""""""""""""""""""

     /verify <verification_code>

    """""""""""""""""""""""""""""""
    @cog_ext.cog_slash(name="verify", description="Verify your email after running the /register command", guild_ids=guild_ids)
    async def _verify(self, ctx: SlashContext, verification_code: str):


        try:
            cursor.execute("SELECT email, COUNT(*) FROM VERIFICATION WHERE createdAt >= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE AND discordId = %s AND code = %s;", (ctx.author.id, verification_code))
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))
        result = cursor.fetchone()
        if (result[1] < 1):
            return await ctx.send(content="The code you entered was incorrect or has expired (5 mins)")

        # Insert a new row into the database 
        try: 
            cursor.execute('INSERT INTO MEMBER (email, discordId) VALUES (%s, %s)', (result[0], ctx.author.id)) 
        except Exception as e:
            return await ctx.send(content="Error: " + str(e))

        # Find the verified role and add it to the user
        try:
            verified_role = utils.get(ctx.guild.roles,name="Verified")
            await ctx.author.add_roles(verified_role)
        except Exception as e:
            return await ctx.send(content="Error: Failed to add role. " + str(e))

        await ctx.send(content="Successfully Registered!")


def setup(bot: Bot):
    bot.add_cog(Schedules(bot))
