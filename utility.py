# utility.py
import discord.ext.commands.bot
import roles

lowerList = [e.casefold() for e in roles.ROLES_LIST]

def getRoleFromString(roleString):
    if roleString.casefold() in lowerList:
        index = lowerList.index(roleInput.casefold())
        newRole = discord.utils.get(message.guild.roles,
                                    name=roles.ROLES_LIST[index])
    else:
        return None
