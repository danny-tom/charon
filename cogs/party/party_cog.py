# party_cog.py
#
# The party cog contains the definition of all the party-related management
# that the bot can perform. The party functionality allows users to create
# an embed message that allows other users to add themselves as a member in
# similar to an in-game lobby.

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.party import party_class as party
from utility import utility, discord_utility


load_dotenv()
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
LFG_CHANNEL = os.getenv('LFG_CHANNEL')


parties = []


class PartyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # party
    #
    # The party command provides the user a way to create an individual
    # embed message that holds a list of members and waitlist. The message can
    # be of a preset type or a custom type. Preset types mention the role while
    # custom types do not. When a user creates a the embed message, other users
    # can interact with the default reactions added by the bot to add
    # themselves or remove themselves from the party. Party leaders have the
    # additional option to close the party early.

    @commands.command(name='party', brief='Creates a party people can join',
                      description=f'\"{COMMAND_PREFIX}party Role\" - '
                      'Creates party creator for specific Role with presets\n \
                      \"{COMMAND_PREFIX}party SomeName OptionalSize\" - '
                      'Creates a custom party of SomeName and OptionalSize '
                      '(default size will be 4)')
    async def createParty(self, context, *args):
        if len(args) == 0:
            return await context.channel.send(
                f'{context.author.name}, please include a party name and '
                f'optional party size (default size is '
                f'{party.DEFAULT_PARTY_SIZE} or preset)')

        name = args[0]

        if name.isspace() or len(name) == 0:
            return await context.channel.send('Please type a valid party name')

        try:
            size = int(args[1]) if len(args) >= 2 else None
        except ValueError:
            return await context.channel.send('Ensure that party size is a'
                                              'number')

        if len(name) > 256:
            return await context.channel.send('Your party name is too long. '
                                              '(256 characters please)')

        if size is not None and size <= 0:
            return await context.channel.send('Your party size is too small.')

        role = utility.getRole(context.guild.roles, name)

        if role is not None and utility.isGamesRole(role):
            message = await context.channel.send(role.mention)
        else:
            message = await context.channel.send(embed=discord.Embed())

        newParty = (party.Party(message, context.author, name) if size is None
                    else party.Party(message, context.author, name, size))
        parties.append(newParty)

        await message.edit(embed=newParty.getEmbed())
        await message.add_reaction(newParty.joinEmoji)
        await message.add_reaction(newParty.closeEmoji)

        # on_reaction_add
        #
        # The party cog looks for users reacting to the party embed messages so
        # when a user click on one of the two reactions, the bot can performs
        # the appropriate action
