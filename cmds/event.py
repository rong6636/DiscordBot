'''處理DISCORD系統'''
'''處理一般聊天對話'''
'''
像是:
    LOL系列
    hi系列
'''

import json
import random

import discord
from discord.ext import commands
from core.classes import Cog_Extension
from cmds.react import React

apex_list = [" Mozambique here!", " My name is \"ready to go\"!", " ALL FATHER GIVE ME SIGHT", " I'm taking fire, friends.", " Recharge my shield!", " 鎖爛啦! 爆甲打肉!", " 幹他!他媽他紅甲!", " 滋蹦!", " 跳哪裡?跳老家!", " 打側腦!", " 救我啊啊啊~ 有人推我", " 我繞一下啊，啊你怎麼倒了?", " 席爾進空投", " 孤狼! 讓他死!", " 隊友是傻逼"]

hi_list = ["HI!", "HI", "Hi!", "Hi", "hi!", "hi", "hello", "hello, world", "Hello, World!"]

with open ('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        WELLCOME_CHANNEL = self.bot.get_channel(int(jdata['WelcomeChannel']))
        await WELLCOME_CHANNEL.send(f'{member} Join!')
        print(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        WELLCOME_CHANNEL = self.bot.get_channel(int(jdata['WelcomeChannel']))
        await WELLCOME_CHANNEL.send(f'{member} Leave!')
        print(f'{member} leave!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.content.upper() == 'HI' or msg.content == '嗨' or msg.content.upper() == 'HI!':
            await msg.channel.send(random.choice(hi_list))
        elif msg.content.upper() == 'LOL' or msg.content.upper() == '打LOL' or msg.content.upper() == 'LOL?':
            await msg.channel.send('@everyone 來打LOL啦!!')
        elif 'APEX' in msg.content.upper() or "欸配可思" in msg.content.upper():
            await msg.channel.send('@everyone' + random.choice(apex_list))
        

def setup(bot):
    bot.add_cog(Event(bot))
