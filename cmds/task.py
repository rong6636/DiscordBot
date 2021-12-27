import json
import random
import pytz

import discord
from discord.ext import commands

import json, asyncio, datetime
from core.classes import Cog_Extension

with open ('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def interval():
            await self.bot.wait_until_ready()
            self.channel01 = self.bot.get_channel(int(jdata['TimeChannelDaTe']))
            self.channel02 = self.bot.get_channel(int(jdata['TimeChannelTime']))
            #self.enable = 1
            while not self.bot.is_closed():
                # Set TimeZone in Taiwan
                ROC = datetime.datetime.now(tz=pytz.timezone('Asia/Taipei'))
                print(ROC)
                
                Date = "民國 " + str(ROC.year-1911) + "年" + str(ROC.month) + "月" + str(ROC.day) + "日"
                Now = "台灣時間" + ROC.strftime(' %H') + "時" + ROC.strftime('%M') + "分"
                await self.channel01.edit(name=Date)
                await self.channel02.edit(name=Now)
                # print(Now)
                # await self.channel.send("Hi im here la!")
                await asyncio.sleep(75) #單位 secand
        
        self.bg_task = self.bot.loop.create_task(interval())
    
    
    @commands.command()
    async def set_TimeChannel_ID(self, ctx, id:int):
        self.channel01 = self.bot.get_channel(id)
        await ctx.send(f"Set Channel Success by {self.channel01.mention}!")
    
    @commands.command()
    async def set_TimeChannel(self, ctx, id:int, en:int):
        #self.enable = en
        self.channel01 = self.bot.get_channel01(id)

        print(f"set_TimeChannelName = {id}")
        print(f"set_TimeChannelEnable = {en}")
    
def setup(bot):
    bot.add_cog(Task(bot))
