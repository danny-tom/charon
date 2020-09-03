# roles_cog.py
#
# The roles cog contains the definition of all the role-related
# management that the bot can perform. This includes the commands
# that uses can use to add/remove themselves to/from a role, listing
# out members currently under specific roles, and roles that can be used
# with the bot.

import os

from discord.ext import commands
from dotenv import load_dotenv

from utility import utility
from rolesJSON import ROLES_JSON


load_dotenv()
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # addRole
    #
    # or if there were issues with assigning the role.

    @commands.command(name='addRole', brief='Add SomeRole to the guild',
                      description=f'\"{COMMAND_PREFIX}addRole SomeRole OptionalSize OptionalEmoji\" - '
                      'Add SomeRole to the guild (default size is 4 and emoji to 👍)')
    async def addRole(self, context, *args):
        if len(args) == 0:
            return await context.channel.send(
                f'{context.author.name}, '
                f'please tell me what role to add')

        roleName = str(args[0])

        size = None
        emoji = None
        imageURL = None

        for arg in args[1:]:
            keyValue = arg.split("=")
            if keyValue[0].casefold() == 'size'.casefold():
                size = int(keyValue[1])
            elif keyValue[0].casefold() == 'emoji'.casefold():
                emoji = str(keyValue[1])
            elif keyValue[0].casefold() == 'imageURL'.casefold():
                imageURL = str(keyValue[1])

        if ROLES_JSON.addRole(context.guild.id, roleName, size, emoji, imageURL):
            return await context.channel.send(
                f'{context.author.name}, '
                f'{roleName} was added.'
            )

        await context.channel.send(
            f'{context.author.name}, '
            f'{roleName} was not added because it already exists.'
        )

    # addRole
    #
    # or if there were issues with assigning the role.

    @commands.command(name='removeRole', brief='Add SomeRole to the guild',
                      description=f'\"{COMMAND_PREFIX}addRole SomeRole OptionalSize OptionalEmoji\" - '
                      'Add SomeRole to the guild (default size is 4 and emoji to 👍)')
    async def removeRole(self, context, *arg):
        if len(arg) == 0:
            return await context.channel.send(
                f'{context.author.name}, '
                f'please tell me what role to delete')

        roleName = str(arg[0])

        if ROLES_JSON.removeRole(context.guild.id, roleName):
            return await context.channel.send(
                f'{context.author.name}, '
                f'{roleName} was removed.'
            )
        
        await context.channel.send(
            f'{context.author.name}, '
            f'{roleName} was not removed because it did not exist.'
        )
    
    # iam
    #
    # The iam command provides the user a way to assign themselves a role in a
    # Discord server without the need to have an admin do so manually.
    # The user can type the command in any channel they have permission
    # to message and if the role they request is one contained in roles.py,
    # the bot grants the role and messages in channel that they have done so
    # or if there were issues with assigning the role.

    @commands.command(name='iam', brief='Add yourself to SomeRole',
                      description=f'\"{COMMAND_PREFIX}iam SomeRole\" - '
                      'Add yourself to SomeRole')
    async def iam(self, context, *arg):
        if len(arg) == 0:
            return await context.channel.send(
                f'{context.author.name}, '
                f'please tell me what role to use for iam')

        role = utility.getRole(context.guild.roles, arg[0])

        if role is None:
            return await context.channel.send(
                f'{context.author.name}, role \'{arg[0]}\' does not exist')

        if not utility.isGamesRole(role):
            return await context.channel.send(
                f'{context.author.name}, {role} is a restricted role')

        if role in context.author.roles:
            return await context.channel.send(
                f'{context.author.name}, but you are already {role}')

        await context.author.add_roles(role)
        await context.channel.send(
            f'{context.author.name}, you are granted {role}')

    # iamnot
    #
    # The iamnot command is the exact opposite of the iam command. The user
    # uses this command to remove a role already assigned to them. The user
    # can type this command in any channel they have permission to message
    # and if the role they want removed is one  contained in  roles.py, the
    # bot removes the roles and messsages in channel that they have done so
    # or if there were issues with removing the role.

    @commands.command(name='iamnot', brief='Remove yourself from SomeRole',
                      description=f'\"{COMMAND_PREFIX}iamnot SomeRole\" - '
                      'Remove yourself from SomeRole')
    async def iamnot(self, context, *arg):
        if len(arg) == 0:
            return await context.channel.send(
                f'{context.author.name}, please tell me what role to use for '
                'iamnot')

        role = utility.getRole(context.guild.roles, arg[0])

        if role is None:
            return await context.channel.send(
                f'{context.author.name}, role \'{arg[0]}\' does not exist')

        if role not in context.author.roles:
            return await context.channel.send(
                f'{context.author.name}, but you were never {role}')

        await context.author.remove_roles(role)
        await context.channel.send(
            f'{context.author.name}, you are removed from {role}')

    # whois
    #
    # The whois command allows the user to see who belongs in each role that
    # is managed by the bot. The user can use this command in any channel they
    # have permission to message and the response is returned in the same
    # channel that it was messaged in.

    @commands.command(name='whois', brief='Prints users belonging to role',
                      description=f'\"{COMMAND_PREFIX}whois SomeRole\" - '
                      'Prints a list of users belonging to SomeRole')
    async def whois(self, context, *arg):
        if len(arg) == 0:
            return await context.channel.send(f'{context.author.name}, '
                                              'please tell me what role to '
                                              'use for whois')

        role = utility.getRole(context.guild.roles, arg[0])

        if role is None:
            return await context.channel.send(
                f'{context.author.name}, role \'{arg[0]}\' does not exist')

        if not utility.isGamesRole(role):
            return await context.channel.send(
                f'{context.author.name}, {role} is a restricted role')

        members = sorted(
            list(member.name for member in role.members), key=str.casefold)

        if len(members) == 0:
            return await context.channel.send(
                f'{context.author.name}, {role} has no users')

        # prepend \n because code block bug removes first member
        memberStr = "\n" + "\n".join(members)
        await context.channel.send(
            f'{context.author.name}, here is the list of users in '
            f'{role} you requested: ```{memberStr}```')

    # games
    #
    # The games command allows the user to see what roles are available that
    # can be later use with the iam and iamnotcommands. The response lists
    # out the all the roles with the count of users currently assigned with
    # the corresponding role.

    @commands.command(name='games', brief='Prints my supported roles',
                      description=f'\"{COMMAND_PREFIX}games\" - '
                      'Prints a list of my supported roles')
    async def games(self, context):
        games = []

        # Variables are used for string formatting purposes
        longestRole = 0
        padding = 1

        # Add valid roles to our display
        for role in context.guild.roles:
            if utility.isGamesRole(role):
                games.append([str(role), str(len(role.members))])
                if len(str(role)) > longestRole:
                    longestRole = len(str(role))

        if len(games) == 0:
            return await context.channel.send(f'{context.author.name}, '
                                              'I manage no games here')

        formatter = "{:<" + str(longestRole + padding) + "}({})\n"
        gamesToStr = ""
        for pair in games:
            gamesToStr += formatter.format(pair[0], pair[1])
        await context.channel.send(f'{context.author.name}, here is a list of '
                                   f'the roles that I manage:'
                                   f'```{gamesToStr}```')
