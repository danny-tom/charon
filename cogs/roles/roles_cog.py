# roles_cog.py
#
# The roles cog contains the definition of all the role-related
# management that the bot can perform. This includes the commands
# that uses can use to add/remove themselves to/from a role, listing
# out members currently under specific roles, and roles that can be used
# with the bot.

import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

from utility import utility


load_dotenv()
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

        if not utility.isGameRole(context.guild, self.bot, role):
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

        if not utility.isGameRole(context.guild, self.bot, role):
            return await context.channel.send(
                f'{context.author.name}, {role} is a restricted role')

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

        if not utility.isGameRole(context.guild, self.bot, role):
            return await context.channel.send(
                f'{context.author.name}, {role} is a restricted role')

        members = sorted(
            list(member.name for member in role.members), key=str.casefold)
        members.remove(self.bot.user.name)

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
            if utility.isGameRole(context.guild, self.bot, role):
                games.append([str(role), str(len(role.members)-1)])
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

    # createRole
    #
    # This is an admin command
    #
    # createRole creates a valid game role. A valid game role
    # is a role that exists on server, has no role permissions,
    # and is manageable by the bot.

    @commands.command(name='createrole',
                      brief='(Admin Only) creates a game role',
                      description=f'\"{COMMAND_PREFIX}createrole SomeRole\" - '
                      'Creates SomeRole on current guild if it does not exist')
    async def createRole(self, context, *arg):
        author = context.author

        if not author.guild_permissions.administrator:
            return await context.channel.send(
                f'{author.name}, you do '
                f'not have permissions to create/delete roles')

        if len(arg) == 0:
            return await context.channel.send(
                f'{author.name}, please specify '
                f'the role you wish to create')

        roleName = str(arg[0]).strip()
        if roleName == "":
            return await context.channel.send(
                f'{author.name}, please specify '
                f'an appropriate role name')

        role = utility.getRole(context.guild.roles, roleName)

        if role is not None:
            return await context.channel.send(
                f'{author.name}, {role.name} '
                f'already exists on server')

        try:
            newRole = await context.guild.create_role(
                name=roleName,
                permissions=discord.Permissions.none(),
                reason=f'Charon Bot: {author.name} created {roleName}'
            )
            await (discord.utils.find(
                lambda m: m == self.bot.user, context.guild.members)
                .add_roles(newRole))
        except discord.Forbidden:
            return await context.channel.send(
                f'{author.name}, I do not '
                f'have permissions to manage roles.'
            )

        await context.channel.send(
            f'{author.name}, {newRole.mention} '
            f'has been added to server')

    # deleteRole
    #
    # This is an admin command
    #
    # deleteRole deletes a valid game role. A valid game role
    # is a role that exists on server, has no role permissions,
    # and is manageable by the bot.

    @commands.command(name='deleterole',
                      brief='(Admin Only) deletes a game role',
                      description=f'\"{COMMAND_PREFIX}deleterole SomeRole\" - '
                      'Deletes SomeRole from the guild')
    async def deleteRole(self, context, *arg):
        author = context.author

        if not author.guild_permissions.administrator:
            return await context.channel.send(
                f'{author.name}, you do '
                f'not have permissions to add/delete roles')

        if len(arg) == 0:
            return await context.channel.send(
                f'{author.name}, please specify '
                f'the games role you wish to delete')

        roleName = str(arg[0]).strip()
        role = utility.getRole(context.guild.roles, roleName)

        if role is None:
            return await context.channel.send(
                f'{author.name}, {roleName} '
                f'does not exist on server')

        roleName = role.name

        if not utility.isGameRole(context.guild, self.bot, role):
            return await context.channel.send(
                f'{author.name}, {roleName} '
                f'is a restricted role')

        try:
            await role.delete(
                reason=f'Charon Bot: {author.name} deleted {roleName}')
        except discord.Forbidden:
            return await context.channel.send(
                f'{author.name}, I do not '
                f'have permissions to manage role {roleName}.'
            )

        await context.channel.send(
                f'{author.name}, {roleName} '
                f'has been deleted from server')
