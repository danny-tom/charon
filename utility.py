# utility.py
import discord.ext.commands.bot
import roles

lowerList = [e.casefold() for e in roles.ROLES_LIST]


def getRoleFromString(ctx, roleString):
    if roleString.casefold() in lowerList:
        index = lowerList.index(roleString.casefold())
        newRole = discord.utils.get(ctx.guild.roles,
                                    name=roles.ROLES_LIST[index])
    else:
        raise ValueError('Invalid role string passed in by user')
