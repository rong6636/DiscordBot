'''
    ### MAIN FUNCTION ###
    ### 版本資訊
        # 1.0
            史前時代，未留紀錄
        # 2.2
            圖片庫增加420%，現在任何訊息含有'抽'字，都會觸發隨機抽圖。",
        # 2.3
            精簡程式碼，準備工作
            預備簡化圖片模組，抽圖 peko
            簡化爬蟲模組
    
    ### 基礎設定
        # 注意地方
            放上repl.it時加上 import keep_alive
            與 在bot.run(jdata['TOKEN'])前面再加上keep_alive.keep_alive()
    
'''
import json
import os
import random
import keep_alive
import discord
from discord.ext import commands

with open ('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(">>偷偷插要用衛生紙 is online<<")
    await bot.change_presence(activity=discord.Game(name = "轉生後當上八星魔王"))


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded "{extension}" done!')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un-Loaded "{extension}" done!')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re-Loaded "{extension}" done!')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    keep_alive.keep_alive()
    bot.run(jdata['TOKEN'])
