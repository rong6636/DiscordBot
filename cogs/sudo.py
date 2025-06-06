
import asyncio
from datetime import datetime, timedelta, timezone
import discord
from discord.ext import commands
from core.classes import Cog_Extension

from config import config

class Sudo(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BOT_NAME = config.get("bot", "name")
        self.BOT_VERSION = config.get("bot", "last_update")
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')


async def setup(bot):
    await bot.add_cog(Sudo(bot))