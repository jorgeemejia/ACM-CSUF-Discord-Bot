from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from os import path
import json
from helpers import getGuilds

guild_ids = getGuilds()

classes_path = path.relpath("data/classes.json")
students_path = path.relpath("data/students.json")

# Example of reading from a json file

with open(classes_path, 'r') as openfile:
    json_object = json.load(openfile)
    print(json_object)


# Example of writing to a json file 

class_test_dict = {
        "CPSC 131-05": ["Aaron"],
        "MATH 338-01": ["Bob", "Kevin"]
}

class_json = json.dumps(class_test_dict)

with open(classes_path, "w") as outfile:
    outfile.write(class_json)

with open(classes_path) as f:
  classes = json.load(f)

with open(students_path) as f:
  students = json.load(f)

class Schedules(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="schedule", name="view", description="View your schedule", guild_ids=guild_ids)
    async def _schedule_view(self, ctx: SlashContext):
        await ctx.send(content="schedule")

    @cog_ext.cog_subcommand(base="schedule", name="add", description="Add a class to your schedule", guild_ids=guild_ids)
    async def _schedule_add(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule add")

    @cog_ext.cog_subcommand(base="schedule", name="remove", description="Remove a class from your schedule", guild_ids=guild_ids)
    async def _schedule_remove(self, ctx: SlashContext, text: str):
        await ctx.send(content="schedule remove")

    # two json files, classes.json, students.json

    # /schedule 
        # open the students.json file
        # return the students classes
        # display button asking to share to the channel

    # /schedule add
        # open both json files
        # validate the input
        # add the class to the person
        # add the person to the class
        # give them the role/permissions
        
    # /schedule remove
        # open both json files
        # check if the student is in that class
        # remove the class from the student
        # remove the student from the class
        # update their roles/permissions
    
    """
    Create your own command that allows a user to run /schedule, and it will return a link to the google form ("https://docs.google.com/forms/d/1sz-YZ3QkpTkVMFYlX8Mt0k1jhJrSY1BPzXMMUVdCEXs/edit")
    Create a description for the command as well.
    """

def setup(bot: Bot):
    bot.add_cog(Schedules(bot))