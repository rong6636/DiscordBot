'''
    2023 04 07 用AI增強code邏輯與可讀性
    2023 04 28 更新discord.py版本 1.7.3 >> 2.2.2

    2023 0821 change token: test -> 姊姊在山上釣鯨魚。 private channel change to public channel
    
    ------ version 3 ------
    # 2025 0606 將機器人從海大實驗室server 移到其他地方跑。 同時更新程式碼。

'''



import os
import random
import asyncio

# 設定 config
from config import config as cfg

# 設定 Discord Bot
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 設定日誌
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot")

async def load_extensions(bot):
    cogs_dir = cfg.get('server', 'cogs_path')
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"Loaded {filename[:-3]}")
            except Exception as e:
                logger.error(f"Failed to load {filename[:-3]}: {e}")

@bot.event
async def on_ready():
    print(f">> {cfg.get('bot', 'name')} is online<<")
    await load_extensions(bot)
    await bot.change_presence(activity=discord.Game(name="轉生後當上八星魔王"))

if __name__ == "__main__":
    bot.run(cfg.get('bot', 'TOKEN'))
