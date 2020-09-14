from discord import Permissions, utils

# utility.py


# returns the role regardless of input case-sensitivity
# returns None if no match can be found
def getRole(roles, roleName):
    return utils.find(
        lambda r: str(r).casefold() == roleName.casefold(), roles)


# Returns True if the role has no permissions and is in the bot roles
def isGameRole(guild, bot, role):
    botMember = utils.find(lambda m: m == bot.user, guild.members)

    if botMember is None or role is None:
        return False

    manageRoles = [r for r in botMember.roles if r.permissions.manage_roles]

    if len(manageRoles) == 0:
        return False

    topManageRole = max(manageRoles, key=lambda r: r.position)

    if (topManageRole is None or
            role not in botMember.roles or
            not role.permissions.is_subset(Permissions.none()) or
            role >= topManageRole):
        return False

    return True
