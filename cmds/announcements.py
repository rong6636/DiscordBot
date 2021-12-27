'''處理BOT公告'''

import json
import random

import discord
from discord.ext import commands
from core.classes import Cog_Extension

with open ('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class announcements(Cog_Extension):
    #版本更新玩記得改Setting.json
    @commands.command()
    async def an(self, ctx):
        print(ctx.author.id)
        if ctx.author.id == int(jdata['MasterID']):
            await ctx.message.delete()
            await ctx.send(str(jdata['UpdateContent']))

    #版本更新中改Setting.json
    @commands.command()
    async def con(self, ctx):
        print(ctx.author.id)
        if ctx.author.id == int(jdata['MasterID']):
            await ctx.message.delete()
            await ctx.send(str(jdata['Construction']))
        


def setup(bot):
    bot.add_cog(announcements(bot))
