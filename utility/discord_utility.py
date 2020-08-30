# discord_utility.py
import discord
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def getChannel(self, guildName, channelName):
        discord.utils.get(commands.bot.get_all_channels(),
                          guild__name=guildName, name=channelName)
