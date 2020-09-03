from datetime import datetime

import discord

import roles

# 86400 seconds in 24 hours
# 43200 seconds in 12 hours
# 14400 seconds in 4 hours
# 3600 seconds in an hour
ACTIVE_DURATION_SECONDS = 14400
DEFAULT_PARTY_SIZE = 4
DEFAULT_JOIN_EMOJI = '👍'
DEFAULT_LEAVE_EMOJI = '❌'


class Party:
    def __init__(self, message, leader, name, size=None):
        self.message = message
        self.__lastUpdatedDateTime = datetime.now()
        self.__partyList = [leader]
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

        self.leaveEmoji = DEFAULT_LEAVE_EMOJI

    @staticmethod
    def __getPreset(name):
        for preset in roles.ROLES_LIST:
            if name.casefold() == preset.name.casefold():
                return preset
        return None

    def __updateTime(self):
        self.__lastUpdatedDateTime = datetime.now()

    def addMember(self, user):
        self.__updateTime()

        if user in self.__partyList or user in self.__waitlist:
            return

        if len(self.__partyList) < self.size:
            self.__partyList.append(user)
        else:
            self.__waitlist.append(user)

    def removeMember(self, user):
        self.__updateTime()

        if user in self.__partyList:
            self.__partyList.remove(user)

        if user in self.__waitlist:
            self.__waitlist.remove(user)

        if len(self.__partyList) < self.size and len(self.__waitlist) > 0:
            self.__partyList.append(self.__waitlist.pop(0))

    def hasMember(self, user):
        if user in self.__partyList:
            return True
        if user in self.__waitlist:
            return True
        return False

    def isInactive(self):
        return ((datetime.now() - self.__lastUpdatedDateTime).total_seconds()
                > ACTIVE_DURATION_SECONDS)

    def isEmpty(self):
        return len(self.__partyList) + len(self.__waitlist) == 0

    def getEmbed(self):
        embed = discord.Embed()
        embed.title = f'{self.name}'
        embed.description = ('Add yourself to the party by using reaction '
                                f'\"{self.joinEmoji}\"\n')
        embed.add_field(
            name=f'Party Members ({len(self.__partyList)}/{self.size})',
            value="\n".join(self.__getNames(self.__partyList)),
            inline=True)
        if (len(self.__waitlist) > 0):
            embed.add_field(
                name='Waitlist',
                value="\n".join(self.__getNames(self.__waitlist)),
                inline=True)
        if self.imageURL is not None:
            embed.set_thumbnail(url=self.imageURL)

        return embed

    @staticmethod
    def __getNames(memberList):
        names = []
        for member in memberList:
            names.append(member.name)
        return names
