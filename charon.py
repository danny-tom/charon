# charon.py
import os
import discord.ext.commands.bot
from dotenv import load_dotenv
import roles


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.ext.commands.Bot('!')


# On any message, if the exact text is '!iam valorant' or
# '!iamnot valorant', the bot will grant the role matching the String
# stored in roles.py. The bot will message on errors such as
# role name not found in server or the bot does not have enough permissions
@bot.event
async def on_message(message):

    for role in roles.ROLES_LIST:
        if message.content == '!iam ' + role.lower():
            try:
                if(role not in message.author.roles):
                    await message.author.add_roles(role)
                    await message.channel.send(f'{message.author.name}, you are'
                                               f' granted {role}')
                else:
                    await message.channel.send(f'{message.author.name}, but you'
                                               f' are already {role}')
            except AttributeError:
                await message.channel.send(f'{message.author.name}, that role does'
                                           ' not exist or I have not been given '
                                           ' permission to grant you that role')

        if message.content == '!iamnot ' + role.lower():
            try:
                if(role in message.author.roles):
                    await message.author.remove_roles(role)
                    await message.channel.send(f'{message.author.name}, you are'
                                               f' removed from {role}')
                else:
                    await message.channel.send(f'{message.author.name}, but were'
                                               f' never {role}')
            except AttributeError:
                await message.channel.send(f'{message.author.name}, that role does'
                                           ' not exist or I have not been given'
                                           ' permission to grant you that role')

bot.run(TOKEN)
