from discord import Permissions

# utility.py


# returns the role regardless of input case-sensitivity
# returns None if no match can be found
def getRole(roles, roleName):
    for r in roles:
        if roleName.casefold() == str(r).casefold():
            return r
    return None


# returns if role is found in guild, has no permissions
# and is manageable by the bot
def isGamesRole(guild, bot, role):
    botMember = None

    # find bot's member object in guild
    for m in guild.members:
        if m == bot.user:
            botMember = m

    if botMember is None:
        return False

    # get the highest role with manage_role permission
    botRole = None
    manageRolePermission = Permissions.none()
    manageRolePermission.manage_roles = True
    for r in botMember.roles:
        if r.permissions.is_superset(manageRolePermission):
            botRole = r
            break

    if botRole is None:
        return False

    # if role is found, has no permissions, and is below
    # bot's manage_role role position, then True
    for r in botMember.roles:
        if (r == role and
                r.position < botRole.position and
                r.permissions.is_subset(Permissions.none())):
            return True

    return False
