# charon.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import roles
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

COMMAND_PREFIX = '.'
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

# returns the role regardless of input case-sensitivity
# returns None if no match can be found
def getRoleID(roles, roleName):
    for r in roles:
        if roleName.lower() == str(r).lower():
            return r
    return None

# restricts roles that can be picked based on roles.py
def isRestrictedRole(role):
    for validRole in roles.ROLES_LIST:
        if validRole.lower() == str(role).lower():
            return False
    return True

# On any message, if the exact text is '.iam valorant' or
# '.iamnot valorant', the bot will grant the role matching the String
# stored in roles.py. The bot will message on errors such as
# role name not found in server or the bot does not have enough permissions
@bot.command(name='iam', brief='Add yourself to SomeRole', 
description=f'''\"{COMMAND_PREFIX}iam SomeRole\" - Add yourself to SomeRole''')
async def iam(context, *arg):
    if len(arg) == 0:
        await context.channel.send(
            f'{context.author.name}, please tell me what role to use for iam')
        return

    role = getRoleID(context.guild.roles, arg[0])

    if role == None:
        await context.channel.send(
            f'{context.author.name}, role \'{arg[0]}\' does not exist')
        return

    if isRestrictedRole(role):
        await context.channel.send(
            f'{context.author.name}, {role} is a restricted role')
        return

    if role in context.author.roles:
        await context.channel.send(
            f'{context.author.name}, but you are already {role}')
    else:
        await context.author.add_roles(role)
        await context.channel.send(
            f'{context.author.name}, you are granted {role}')
        
@bot.command(name='iamnot', brief='Remove yourself from SomeRole',
description=f'''\"{COMMAND_PREFIX}iamnot SomeRole\" - Remove yourself from SomeRole''')
async def iamnot(context, *arg):
    if len(arg) == 0:
        await context.channel.send(
            f'{context.author.name}, please tell me what role to use for iamnot')
        return

    role = getRoleID(context.guild.roles, arg[0])

    if role == None:
        await context.channel.send(
            f'{context.author.name}, role \'{arg[0]}\' does not exist')
        return

    if role in context.author.roles:
        await context.author.remove_roles(role)
        await context.channel.send(
            f'{context.author.name}, you are removed from {role}')
    else:
        await context.channel.send(
            f'{context.author.name}, but you were never {role}')

@bot.command(name='whois', brief='Prints users belonging to role',
description=f'''\"{COMMAND_PREFIX}whois SomeRole\" - Prints a list of users belonging to SomeRole''')
async def whois(context, *arg):
    if len(arg) == 0:
        await context.channel.send(
            f'{context.author.name}, please tell me what role to use for whois')
        return

    role = getRoleID(context.guild.roles, arg[0])

    if role == None:
        await context.channel.send(
            f'{context.author.name}, role \'{arg[0]}\' does not exist')
        return

    members = sorted(list(member.name for member in role.members), key=str.casefold)

    if len(members) == 0:
        await context.channel.send(
            f'{context.author.name}, {role} has no users')
        return

    memberStr = "\n".join(members)

    await context.channel.send(
        f'{context.author.name}, here is the list of users in '
        f'{role} you requested:'
        f'```{memberStr}```')

# Lists out games supported 
@bot.command(name='games', brief='Prints my supported roles',
description=f'''\"{COMMAND_PREFIX}games\" - Prints a list of my supported roles''')
async def games(context):
    games = []

    # Variables are used for string formatting purposes
    longestRole = 0
    padding = 1

    # Add valid roles to our display
    for role in context.guild.roles:
        if not isRestrictedRole(role):
            games.append([str(role), str(len(role.members))])
            if len(str(role)) > longestRole:
                longestRole = len(str(role))

    if len(games) == 0:
        await context.channel.send(f'{context.author.name}, I manage no games here')
        return
    
    formatter = "{:<"+str(longestRole+padding)+"}({})\n"
    gamesToStr = ""
    for pair in games:
        gamesToStr += formatter.format(pair[0], pair[1])
    await context.channel.send(f'{context.author.name}, here is a list of the' \
        f' roles that I manage: ```{gamesToStr}```')

@bot.event
async def on_member_join(member):
    # Pick text channel that is top of the list. Can change to check for Continental in future patch
    textChannel = list(filter(lambda x: x.type == discord.ChannelType.text and x.position == 0, member.guild.channels))[0]
    # For flavor, pick a random number of days
    numDays = random.randrange(1, 366)
    await textChannel.send(
        f'Welcome to the Continental, {member.mention}.\n'
        f'My name is Charon. I see you will be staying with us for {numDays} day{"s" if numDays > 1 else ""}.\n'
        f'Feel free to dial \"{COMMAND_PREFIX}help\" if you require any assistance.\n'
        f'...and as always, it is a pleasure having you with us again, {member.name}.')

bot.run(TOKEN)