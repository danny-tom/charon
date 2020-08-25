# roles.py

# This file contains the names of the roles that you want the bot to be
# able to add/remove for users in your server. Each role will need a constant
# and then be added to the list. (i.e. follow the format)
# In your Discord Server, make sure the role name is matching exactly and that
# the bot role is above the role you want it to manage.

class Charon_Role:
    def __init__(self, name=None, size=4, emoji='👍', imageURL=None):
        self.name = name
        self.size = size
        self.emoji = emoji
        self.imageURL = imageURL

VALORANT = Charon_Role(
    name='Valorant',
    size=5, 
    emoji='🔫',
    imageURL='https://vignette.wikia.nocookie.net/leagueoflegends/images/8/88/Valorant_icon.png/revision/latest?cb=20200302105445')

OVERWATCH = Charon_Role(
    name='Overwatch',
    size=6,
    emoji='🎯',
    imageURL='https://vignette.wikia.nocookie.net/overwatch/images/5/53/Pi_defaultblack.png/revision/latest/top-crop/width/220/height/220?cb=20160704195235')

PROJECTWINTER = Charon_Role(
    name='ProjectWinter',
    size=8,
    emoji='❄️',
    imageURL='https://pbs.twimg.com/profile_images/1084835909185372160/QzmW7PC8.jpg')

ROLES_LIST = [
    VALORANT,
    OVERWATCH,
    PROJECTWINTER
    ]