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
    # Only performs actions on messages that start with !iam
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

bot.run(TOKEN)
