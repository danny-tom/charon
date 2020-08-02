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

    valorantRole = discord.utils.get(message.guild.roles, name=roles.VALORANT)

    if message.content == '!iam valorant':
        try:
            if(valorantRole not in message.author.roles):
                await message.author.add_roles(valorantRole)
                await message.channel.send(f'{message.author.name}, you are'
                                           f' granted {roles.VALORANT}')
            else:
                await message.channel.send(f'{message.author.name}, but you'
                                           f' are already {roles.VALORANT}')
        except AttributeError:
            await message.channel.send(f'{message.author.name}, that role does'
                                       ' not exist or I have not been given '
                                       ' permission to grant you that role')

    if message.content == '!iamnot valorant':
        try:
            if(valorantRole in message.author.roles):
                await message.author.remove_roles(valorantRole)
                await message.channel.send(f'{message.author.name}, you are'
                                           f' removed from {roles.VALORANT}')
            else:
                await message.channel.send(f'{message.author.name}, but were'
                                           f' never {roles.VALORANT}')
        except AttributeError:
            await message.channel.send(f'{message.author.name}, that role does'
                                       ' not exist or I have not been given'
                                       ' permission to grant you that role')

bot.run(TOKEN)
