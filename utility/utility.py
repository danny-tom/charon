# utility.py
from roles import ROLES_LIST


# returns the role regardless of input case-sensitivity
# returns None if no match can be found
def getRole(roles, roleName):
    for r in roles:
        if roleName.casefold() == str(r).casefold():
            return r
    return None


# restricts roles that can be picked based on roles.py
def isGamesRole(role):
    for validRole in ROLES_LIST:
        if validRole.name.casefold() == str(role).casefold():
            return True
    return False
