# charon.py
import logging
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.roles.roles_cog import RolesCog
from cogs.party.party_cog import PartyCog


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


bot = commands.Bot(command_prefix=COMMAND_PREFIX)
logging.basicConfig(level=logging.INFO)


# Cogs that the bot needs to load when starting. Each cog is found within the
# "charon/cogs" directory with each cog in their own folder
bot.add_cog(RolesCog(bot))
bot.add_cog(PartyCog(bot))


@bot.event
async def on_member_join(member):
    # Pick text channel that is top of the list.
    # Can change to check for Continental in future patch
    textChannel = list(filter(
        lambda x: (x.type == discord.ChannelType.text
                   and x.position == 0), member.guild.channels))[0]
    # For flavor, pick a random number of days
    numDays = random.randrange(1, 366)
    await textChannel.send(
        f'Welcome to the Continental, {member.mention}.\n'
        f'My name is Charon. I see you will be staying with us for {numDays} '
        f'day{"s" if numDays > 1 else ""}.\nFeel free to dial '
        f'\"{COMMAND_PREFIX}help\" if you require any assistance.\n'
        f'...and as always, it is a pleasure having you with us again, '
        f'{member.name}.')


bot.run(TOKEN)
