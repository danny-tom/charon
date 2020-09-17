# party_cog.py
#
# The party cog contains the definition of all the party-related management
# that the bot can perform. The party functionality allows users to create
# an embed message that allows other users to add themselves as a member in
# similar to an in-game lobby.

import os

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

from cogs.party import party_class as party
from utility import utility


load_dotenv()
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
LFG_CHANNEL = os.getenv('LFG_CHANNEL')
BACKGROUND_LOOP_TIME = os.getenv('BACKGROUND_LOOP_TIME')


parties = []


class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_lfg_channel.start()

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
                      'Creates party creator for specific Role with presets\n'
                      f'\"{COMMAND_PREFIX}party SomeName OptionalSize\" - '
                      'Creates a custom party of SomeName and OptionalSize '
                      '(default size will be 4)')
    async def createParty(self, context, *args):
        # For valid parties, the embed message should go into a specified
        # channel so that regular channels are not moving the embed message
        # from chatter
        lfgChannel = discord.utils.get(self.bot.get_all_channels(),
                                       guild__name=context.guild.name,
                                       name=LFG_CHANNEL)

        if lfgChannel is None:
            return await context.channel.send(f'This server has not set up a'
                                              'LFG Channel (default:'
                                              f' {LFG_CHANNEL})')

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

        newParty = (party.Party(context.author, name) if
                    size is None
                    else party.Party(context.author, name, size))

        messageArgs = {"embed": newParty.getEmbed()}

        if newParty.imageURL is not None:
            messageArgs["file"] = discord.File(
                party.IMAGE_PATH + newParty.imageURL,
                filename=newParty.imageURL)
        if utility.isGameRole(context.guild, self.bot, role):
            messageArgs["content"] = role.mention

        try:
            message = await lfgChannel.send(**messageArgs)
        except discord.Forbidden:
            return await context.channel.send(f'I do not have permissions in'
                                              f' {lfgChannel.mention}')

        newParty.message = message
        parties.append(newParty)

        await message.add_reaction(newParty.joinEmoji)
        await message.add_reaction(newParty.leaveEmoji)

        await context.channel.send(f'Party \'{newParty.name}\' created in'
                                   f' {lfgChannel.mention}')

    # on_reaction_add
    #
    # The party cog looks for users reacting to the party embed messages so
    # when a user clicks on one of the two reactions, the bot can perform
    # the appropriate action. When the user adds a join reaction, they are
    # added to the party or waitlist. When the user adds a leave reaction,
    # they are removed from the party or waitlist.

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        p = self.__findParty(reaction.message)

        if p is None:
            return

        if p.joinEmoji == reaction.emoji and not p.hasMember(user):
            p.addMember(user)
            await reaction.message.edit(embed=p.getEmbed())
        elif p.leaveEmoji == reaction.emoji and p.hasMember(user):
            p.removeMember(user)
            if p.isEmpty():
                parties.remove(p)
                return await reaction.message.delete()
            await reaction.message.edit(embed=p.getEmbed())
        await reaction.remove(user)

    # __findParty
    #
    # This helper function returns a party based on
    # a message input; Otherwise, returns None

    @staticmethod
    def __findParty(message):
        for p in parties:
            if p.message.id == message.id:
                return p
        return None

    # purgeLFGChannelMessage
    #
    # This helper function deletes all messages from
    # LFG_Channel that is not associated with a party

    def purgeLFGChannelMessage(self, message):
        return self.__findParty(message) is None

    # update_lfg_channel
    #
    # This function cleans the lfg_channel of all messages
    # that are not associated with a party. It will also close
    # inactive parties and remove them from the parties list
    # and delete the related message

    @tasks.loop(seconds=int(BACKGROUND_LOOP_TIME))
    async def update_lfg_channel(self):
        for guild in self.bot.guilds:
            lfgChannel = discord.utils.get(guild.channels, name=LFG_CHANNEL)
            if lfgChannel is not None:
                await lfgChannel.purge(check=self.purgeLFGChannelMessage)

        for p in parties:
            if p.isInactive():
                parties.remove(p)
                await p.message.delete()
