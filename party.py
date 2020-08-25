import roles
import discord
from datetime import datetime

# 86400 seconds in 24 hours
# 43200 seconds in 12 hours
# 3600 seconds in an hour
ACTIVE_DURATION_SECONDS = 86400
DEFAULT_PARTY_SIZE = 4
DEFAULT_JOIN_EMOJI = '👍'
DEFAULT_CLOSE_EMOJI = '❌'

class party:
    def __init__(self, message, leader, name, size=None):
        self.__close = False
        self.__message = message
        self.__leader = leader
        self.__creationDateTime = datetime.now()
        self.__partyList = [leader.name]
        self.__waitlist = []

        preset = self.__getPreset(name)

        if (preset is not None):
            self.name = preset.name
            self.size = preset.size if size is None else size
            self.imageURL = preset.imageURL
            self.joinEmoji = preset.emoji
        else:
            self.name = name
            self.size = DEFAULT_PARTY_SIZE if size is None else size
            self.imageURL = None
            self.joinEmoji = DEFAULT_JOIN_EMOJI

        self.closeEmoji = DEFAULT_CLOSE_EMOJI

    @staticmethod
    def __getPreset(name):
        for preset in roles.ROLES_LIST:
            if name.lower() == preset.name.lower():
                return preset
        return None

    def addMember(self, name):
        if name in self.__partyList or name in self.__waitlist:
            return

        if len(self.__partyList) < self.size:
            self.__partyList.append(name)
        else:
            self.__waitlist.append(name)

    def removeMember(self, name):
        if name in self.__partyList:
            self.__partyList.remove(name)

        if name in self.__waitlist:
            self.__waitlist.remove(name)

        if len(self.__partyList) < self.size and len(self.__waitlist) > 0:
            self.__partyList.append(self.__waitlist.pop(0))

    def isMatchJoinEmoji(self, reaction):
        return (self.__message.id == reaction.message.id
                and self.joinEmoji == reaction.emoji)

    def isMatchCloseEmoji(self, reaction, user):
        return (self.__message.id == reaction.message.id
                and self.closeEmoji == reaction.emoji
                and self.__leader.name == user.name)

    def isInactive(self):
        return (datetime.now() - self.__creationDateTime).total_seconds() > ACTIVE_DURATION_SECONDS

    def close(self):
        self.__close = True

    def getEmbed(self):
        embed = discord.Embed()

        if self.__close:
            embed.title = f'{self.name} (Closed)'
            embed.description = f'This party was closed by {self.__leader.name}'
        elif self.isInactive():
            embed.title = f'{self.name} (Inactive)'
            embed.description = f'This party is inactive because it is old.\nPlease create a new party'
        else:
            embed.title = f'{self.name}'
            embed.description = f'Add yourself to the party by using reaction \"{self.joinEmoji}\"\n'
            embed.add_field(
                name=f'Party Members ({len(self.__partyList)}/{self.size})', 
                value="\n".join(self.__partyList) if len(self.__partyList) > 0 else '👻...', 
                inline=True)
            if (len(self.__waitlist) > 0):
                embed.add_field(
                    name=f'Waitlist', 
                    value="\n".join(self.__waitlist), 
                    inline=True)
            if self.imageURL is not None:
                embed.set_thumbnail(url=self.imageURL)

        return embed