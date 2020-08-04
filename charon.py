# charon.py
import os
import discord.ext.commands.bot
from dotenv import load_dotenv
import roles
import utility


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.ext.commands.Bot('!')

lowerList = [e.casefold() for e in roles.ROLES_LIST]


# !iam
# Assigns user a role if the argument matches one in roles.py
@bot.command(name='iam', help='Self-assign yourself a role. Usage:'
             ' !iam [role name]')
async def iam(ctx, *, args):
    try:
        newRole = utility.getRoleFromString(ctx, args)
    except ValueError:
        await ctx.send(f'{ctx.author.name}, that role does not exist or'
                       ' I have not been given permission to grant you that'
                       ' role')
    if(newRole not in ctx.author.roles):
        await ctx.author.add_roles(newRole)
        await ctx.send(f'{ctx.author.name}, you are granted {newRole.name}')
    else:
        await ctx.send(f'{ctx.author.name}, but you are already'
                       f' {newRole.name}')


# !iamnot
# Removes a role from a user if the argument matches one in roles.py
@bot.command(name='iamnot', help='Remove yourself from a role. Usage:'
             ' !iamnot [role name]')
async def iamnot(ctx, *, args):
    try:
        newRole = utility.getRoleFromString(ctx, args)
    except ValueError:
        await ctx.send(f'{ctx.author.name}, that role does not exist or'
                       ' I have not been given permission to remove that'
                       ' role')
        if(newRole in ctx.author.roles):
            await ctx.author.remove_roles(newRole)
            await ctx.send(f'{ctx.author.name}, you are removed from'
                           f' {newRole.name}')
        else:
            await ctx.send(f'{ctx.author.name}, but you were never'
                           f' {newRole.name}')


# !whois
# Outputs a list of users that have a specific role. List is sorted
# alphabetically by name
@bot.command(name='whois', help='Outputs a list of users that have a specific'
             ' role. Usage: !whois [role name]')
async def whois(ctx, *, args):
    try:
        searchedRole = utility.getRoleFromString(ctx, args)
    except ValueError:
        await ctx.channel.send(
            f'{ctx.author.name}, that role does not exist or I have'
            ' not been given permission to give you that information')
        return

    if args.casefold() in lowerList:
        membersList = searchedRole.members
        membersWithRole = list(member.name for member in membersList)
        sortedList = sorted(membersWithRole, key=str.casefold)
        membersWithRoleStr = "\n"
        membersWithRoleStr = membersWithRoleStr.join(sortedList)
        await ctx.send(f'{ctx.author.name}, here is the list of users in'
                       f' {searchedRole} you requested:'
                       f' ```{membersWithRoleStr}```')


# !games
# Outputs a list of roles that the bot recognizes from the Discord server
@bot.command(name='games', help='Outputs a list of the supported games. Usage: !games')
async def games(ctx):
    sortedList = sorted(roles.ROLES_LIST, key=str.casefold)
    registeredUsersList = []
    newGamesList = []

    try:
        for role in sortedList:
            if discord.utils.get(ctx.guild.roles, name=role) is None:
                pass
            else:
                registeredUsers = len(discord.utils.get(
                    ctx.guild.roles, name=role).members)
                newGamesList.append(role)
                registeredUsersList.append(registeredUsers)

        gameAndCount = list(zip(newGamesList, registeredUsersList))
        gameAndCountStr = "\n"

        for pair in gameAndCount:
            gameAndCountStr += pair[0] + '\t(' + str(pair[1]) + ')\n'

        outputString = f'{ctx.author.name}, here is a list of the' \
            f' roles that I manage: ```{gameAndCountStr}```'

        if len(gameAndCount) == 0:
            await ctx.send(f'{ctx.author.name}, I manage no games here')
        else:
            await ctx.send(outputString)

    except AttributeError:
        await ctx.send(
            f'{ctx.author.name}, there was an issue finding the games'
            'that this server supports')


bot.run(TOKEN)
