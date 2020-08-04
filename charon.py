# charon.py
import os
import discord.ext.commands.bot
from dotenv import load_dotenv
import roles


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '.'

bot = discord.ext.commands.Bot(COMMAND_PREFIX)

lowerList = [e.casefold() for e in roles.ROLES_LIST]

# On any message, if the exact text is '.iam valorant' or
# '.iamnot valorant', the bot will grant the role matching the String
# stored in roles.py. The bot will message on errors such as
# role name not found in server or the bot does not have enough permissions

def iam_helper(message):
    roleInput = message.content.split(" ", 1)[1]
    # Ignore case sensitivity for the role
    if roleInput.casefold() in lowerList:
        roleIndex = lowerList.index(roleInput.casefold())
        newRole = discord.utils.get(message.guild.roles,
                                    name=roles.ROLES_LIST[roleIndex])
        return True, newRole, roleIndex
    return False, "", -1

async def iam(message):
    try:
        role_found, newRole, index = iam_helper(message)

        if (role_found):
            try:
                if(newRole not in message.author.roles):
                    await message.author.add_roles(newRole)
                    await message.channel.send(
                        f'{message.author.name}, you are granted'
                        f' {roles.ROLES_LIST[index]}')
                else:
                    await message.channel.send(
                        f'{message.author.name}, but you are already'
                        f' {roles.ROLES_LIST[index]}')
            except AttributeError:
                await message.channel.send(
                    f'{message.author.name}, that role does not exist or'
                    ' I have not been given permission to grant you that'
                    ' role')
        else:
            await message.channel.send(
                f'{message.author.name}, that role does not exist')
    except IndexError:
        await message.channel.send(
            f'{message.author.name}, please tell me what role to use for iam')


async def iamnot(message):
    try:
        role_found, newRole, index = iam_helper(message)
            
        if (role_found):
            try:
                if(newRole in message.author.roles):
                    await message.author.remove_roles(newRole)
                    await message.channel.send(
                        f'{message.author.name}, you are removed from'
                        f' {roles.ROLES_LIST[index]}')
                else:
                    await message.channel.send(
                        f'{message.author.name}, but you were never'
                        f' {roles.ROLES_LIST[index]}')
            except AttributeError:
                await message.channel.send(
                    f'{message.author.name}, that role does not exist or I'
                    'have not been given permission to grant you that'
                    ' role')
        else:
            await message.channel.send(
                f'{message.author.name}, that role does not exist')
    except IndexError:
        await message.channel.send(
            f'{message.author.name}, please tell me what role to use for iamnot')

async def whois(message):
    # After the command, the 2nd part is the role name
    try:
        roleInput = message.content.split(" ", 1)[1]

        # Ignore case sensitivity for the role
        # Check if the bot has should be able to give that particular role
        # information
        try:
            index = lowerList.index(roleInput.casefold())
            searchedRole = discord.utils.get(message.guild.roles,
                                                name=roles.ROLES_LIST[index])
        except ValueError:
            await message.channel.send(
                f'{message.author.name}, that role does not exist or I have'
                ' not been given permission to give you that information')

        if roleInput.casefold() in lowerList:
            try:
                membersList = searchedRole.members
                membersWithRole = list(member.name for member in membersList)
                sortedList = sorted(membersWithRole, key=str.casefold)
                membersWithRoleStr = "\n"
                membersWithRoleStr = membersWithRoleStr.join(sortedList)
                await message.channel.send(
                    f'{message.author.name}, here is the list of users in'
                    f' {roles.ROLES_LIST[index]} you requested:'
                    f'```{membersWithRoleStr}```')
            except AttributeError:
                await message.channel.send(
                    f'{message.author.name}, that role does not exist or I'
                    ' have not been given permission to give you that'
                    ' information')
    except IndexError:
        await message.channel.send(
            f'{message.author.name}, please tell me what role to use for whois')

async def games(message):
    sortedList = sorted(roles.ROLES_LIST, key=str.casefold)
    registeredUsersList = []
    newGamesList = []

    try:
        for role in sortedList:
            if discord.utils.get(message.guild.roles, name=role) is None:
                pass
            else:
                registeredUsers = len(discord.utils.get(
                    message.guild.roles, name=role).members)
                newGamesList.append(role)
                registeredUsersList.append(registeredUsers)

        gameAndCount = list(zip(newGamesList, registeredUsersList))
        gameAndCountStr = "\n"

        for pair in gameAndCount:
            gameAndCountStr += pair[0] + '\t(' + str(pair[1]) + ')\n'

        outputString = f'{message.author.name}, here is a list of the' \
            f' roles that I manage: ```{gameAndCountStr}```'

        if len(gameAndCount) == 0:
            await message.channel.send(f'{message.author.name}, I manage'
                                        ' no games here')
        else:
            await message.channel.send(outputString)

    except AttributeError:
        await message.channel.send(
            f'{message.author.name}, there was an issue finding the games'
            'that this server supports')


async def charon_help(message):
    command_list = '\n'+'\n'.join(LIST_OF_COMMANDS.keys())

    if (message.content.count(" ") is 1):
        command = message.content.split(" ")[1]
        if (command in LIST_OF_COMMANDS.keys()):
            await message.channel.send(f'{message.author.name}, here is what I know' 
                f' about {command}: ```{LIST_OF_COMMANDS[command].__doc__}```')
        else:
            await message.channel.send(f'{message.author.name}, I have not heard of ' 
                'that command. Here is a list of the commands that I know:'
                f'```{command_list}```')
    else:
        await message.channel.send(f'{message.author.name}, Here is a list of the '
            f'commands that I know: ```{command_list}```')


LIST_OF_COMMANDS = {
    "iam":iam,
    "iamnot":iamnot,
    "whois":whois,
    "games":games,
    "help":charon_help
                    }

iam.__doc__ = f'''Usage: \"{COMMAND_PREFIX}iam SomeRole\" - Add yourself to SomeRole'''
iamnot.__doc__ = f'''Usage: \"{COMMAND_PREFIX}iamnot SomeRole\" - Remove yourself from SomeRole'''
whois.__doc__ = f'''Usage: \"{COMMAND_PREFIX}whois SomeRole\" - Prints a list of users belonging to SomeRole'''
games.__doc__ = f'''Usage: \"{COMMAND_PREFIX}games\" - Prints a list of my supported roles'''
charon_help.__doc__ = f'''Usage: \"{COMMAND_PREFIX}help\" - Prints a list of supported commands\n\
    \"{COMMAND_PREFIX}help SomeCommand\" - Prints help for SomeCommand'''

@bot.event
async def on_message(message):
    # Messages that should bring up the "unrecognized command" reply: ".foo", "."
    # Messages that should not: "..", "..."
    if message.content.startswith(COMMAND_PREFIX):
        command = message.content.split(" ")[0][1:]
        if command in LIST_OF_COMMANDS.keys():
            # See above for command functions
            await LIST_OF_COMMANDS[command](message)
        elif not command.startswith(COMMAND_PREFIX):
            await message.channel.send(
                f'{message.author.name}, that is an unrecognized command. '
                f'For a list of supported commands, please send \"{COMMAND_PREFIX}help\"')

bot.run(TOKEN)
