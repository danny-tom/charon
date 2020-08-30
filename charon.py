# charon.py
import logging
import os
import random

import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

from cogs.roles.roles_cog import RolesCog
from cogs.party.party_cog import PartyCog, parties
# from utility import discord_utility as Utility


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
BACKGROUND_LOOP_TIME = os.getenv('BACKGROUND_LOOP_TIME')


bot = commands.Bot(command_prefix=COMMAND_PREFIX)
logging.basicConfig(level=logging.INFO)


# Cogs that the bot needs to load when starting. Each cog is found within the
# "charon/cogs" directory with each cog in their own folder
bot.add_cog(RolesCog(bot))
bot.add_cog(PartyCog(bot))

# bot.add_cog(Utility(bot))


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


@bot.event
async def on_reaction_add(reaction, user):
    global parties
    print('parties:', parties)
    for p in parties:
        print('user.name:', user.name, 'bot.user.name:',
              bot.user.name)
        if user.name == bot.user.name:
            continue
        if p.isMatchJoinEmoji(reaction):
            p.addMember(user.name)
            await reaction.message.edit(embed=p.getEmbed())
            break
        if p.isMatchCloseEmoji(reaction, user):
            p.close()
            await reaction.message.edit(embed=p.getEmbed())
            parties.remove(p)
            break

        # on_reaction_remove
        #
        # The party cog looks for users reacting to the party embed messages so
        # when a user click on one of the two reactions, the bot can performs
        # the appropriate action.


@bot.event
async def on_reaction_remove(reaction, user):
    for p in parties:
        if p.isMatchJoinEmoji(reaction):
            p.removeMember(user.name)
            await reaction.message.edit(embed=p.getEmbed())
            break


# This function checks if parties are inactive
# and cleans up them up if they are
@tasks.loop(seconds=int(BACKGROUND_LOOP_TIME))
async def update_parties():
    for p in parties:
        if p.isInactive():
            await p.message.edit(embed=p.getEmbed())
            parties.remove(p)

update_parties.start()
bot.run(TOKEN)
