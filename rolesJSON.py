import json

ROLES_FILE_PATH = 'data/roles.json'
DEFAULT_PARTY_SIZE = 4
DEFAULT_EMOJI = '👍'
DEFAULT_IMAGE_URL = None

# rolesJSON handles all the interfacing with the roles.json file
# as well as store a cached version of the contents for 
# quick retrieval roles.json will record the guilds 
# and their game roles with retricted server-permission

class rolesJSON:
    def __init__(self, fileURL):
        with open(ROLES_FILE_PATH, 'r') as f:
            self.JSON = json.load(f)

    #
    # Public Functions
    #

    # addRole
    #
    # 

    def addRole(self, guildID, name, size, emoji, imageURL):
        roleName = name
        roleSize = size if size is not None else DEFAULT_PARTY_SIZE
        roleEmoji = emoji if emoji is not None else DEFAULT_EMOJI
        roleImageURL = imageURL if imageURL is not None else DEFAULT_IMAGE_URL

        guild = self.getGuild(guildID)
        
        if guild is None:
            role = self.createRole(roleName, roleSize, roleEmoji, roleImageURL)
            self.JSON['guilds'].append(self.createGuild(guildID, [role]))
            self.updateJSON()
            return True

        role = self.getRole(guildID, roleName)

        if role is None:
            print('create role')
            guild['roles'].append(
                self.createRole(roleName, roleSize, roleEmoji, roleImageURL))
            self.updateJSON()
            return True

        roleChanged = False
        if role["size"] != roleSize:
            print('match')
            role["size"] = roleSize
            roleChanged = True
        if role["emoji"] != roleEmoji:
            role["emoji"] = roleEmoji
            roleChanged = True
        if role["imageURL"] != roleImageURL:
            role["imageURL"] = roleImageURL
            roleChanged = True

        if roleChanged:   
            self.updateJSON()
            
        return roleChanged

    def removeRole(self, guildID, roleName):
        guild = self.getGuild(guildID)

        if guild is None:
            return False

        role = self.getRole(guildID, roleName)

        if role is None:
            return False
        
        if len(guild['roles']) == 1:
            self.JSON['guilds'].remove(guild)
            self.updateJSON()
            return True

        guild['roles'].remove(role)
        self.updateJSON()
        return True

    # getRole
    #
    # retrieves role from guild based on roleName; otherwise None

    def getRole(self, guildID, roleName):
        g = self.getGuild(guildID)
        
        if g is None:
            return None

        for r in g['roles']:
            if r['name'].casefold() == roleName.casefold():
                return r
        return None

    #
    # Helper Functions
    #

    # getGuild
    #
    # retrieves guild based on guildID; otherwise None

    def getGuild(self, guildID):
        for g in self.JSON['guilds']:
            if g['guild_id'] == guildID:
                return g
        return None

    # createGuild
    #
    # creates JSON-friendly guild object

    def createGuild(self, guildID, roles=[]):
        return {
            "guild_id": guildID,
            "roles": roles
        }

    # createRole
    #
    # creates JSON-friendly role object

    def createRole(self, name, size, emoji, imageURL):
        return {
            "name": name,
            "size": size,
            "emoji": emoji,
            "imageURL": imageURL
        }

    # updateJSON
    #
    # updates JSON file with current cached JSON. This method
    # should be called whenever the cached JSON changes.

    def updateJSON(self):
        with open(ROLES_FILE_PATH, "w") as f:
            json.dump(self.JSON, f)

ROLES_JSON = rolesJSON(ROLES_FILE_PATH)