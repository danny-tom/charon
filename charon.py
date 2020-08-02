# charon.py
import os
import discord.ext.commands.bot
from dotenv import load_dotenv
import roles


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.ext.commands.Bot('!')

lowerList = [e.casefold() for e in roles.ROLES_LIST]

# On any message, if the exact text is '!iam valorant' or
# '!iamnot valorant', the bot will grant the role matching the String
# stored in roles.py. The bot will message on errors such as
# role name not found in server or the bot does not have enough permissions
@bot.event
async def on_message(message):
    # !iam/!iamnot
    # This is the primary use of the bot. Assignment based on the messages
    # that people type
    if message.content.startswith('!iam'):
        # After the command, the 2nd part is the role name
        roleInput = message.content.split(" ", 1)[1]

        # Ignore case sensitivity for the role
        if roleInput.casefold() in lowerList:
            index = lowerList.index(roleInput.casefold())
            newRole = discord.utils.get(message.guild.roles,
                                        name=roles.ROLES_LIST[index])

            # !iamnot logic
            if message.content.startswith('!iamnot'):
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

            # !iam logic
            elif message.content.startswith('!iam'):
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

    # !whois
    # Outputs list of users that that a specific role
    if message.content.startswith('!whois'):
        # After the command, the 2nd part is the role name
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
                    f' {roles.ROLES_LIST[index]} you requested\n'
                    f'```{membersWithRoleStr}```')
            except AttributeError:
                await message.channel.send(
                    f'{message.author.name}, that role does not exist or I'
                    ' have not been given permission to give you that'
                    ' information')

    # !games
    # Outputs list of roles that the bot recognizes from the Discord server
    if message.content == '!games':
        try:
            sortedList = sorted(roles.ROLES_LIST, key=str.casefold)
            registeredUsersList = []
            for role in sortedList:
                registeredUsers = len(discord.utils.get(message.guild.roles,
                                                        name=role).members)
                registeredUsersList.append(registeredUsers)

            gameAndCount = list(zip(sortedList, registeredUsersList))
            gameAndCountStr = "\n"

            for pair in gameAndCount:
                gameAndCountStr += pair[0] + '\t(' + str(pair[1]) + ')\n'

            outputString = f'{message.author.name}, here is a list of the' \
                f' roles that I manage ```{gameAndCountStr}```'

            await message.channel.send(outputString)

        except AttributeError:
            await message.channel.send(
                f'{message.author.name}, that role does not exist or I'
                ' have not been given permission to give you that'
                ' information')


bot.run(TOKEN)
