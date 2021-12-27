"""
2021/07/08
讓機器人報告地震資訊

opendata link >> https://opendata.cwb.gov.tw/dataset/observation?page=1

"""
from core.classes import Cog_Extension
import discord
from discord.ext import commands


# 引入 requests 模組
import requests as req
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
# 引入 re 模組
import re
# thread時間
import asyncio
import random
import time

earthquake_list = ["目前發生有感地震! 請注意自身安全!", "有人感受到地震正在發生! 請注意安全! ", "感受到地震正在發生，請注意周遭環境! ", "請注意自身安全! "]

class earthquake_report(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ========全域變數區======== #
        
        # ========================= #

        # 從交通部中央氣象局opendata 取得地震資料
        # 並回傳報告內容
    def get_earthquake_soup():
        #抓取網頁的連結
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-6EA7A397-8B9A-4BE1-BE4D-9A0F69AB0161&format=XML&areaName=%E6%96%B0%E5%8C%97%E5%B8%82"
        response = req.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        return soup
    def get_earthquake_last_reportNum():
        #抓取網頁的連結
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-6EA7A397-8B9A-4BE1-BE4D-9A0F69AB0161&format=XML&areaName=%E6%96%B0%E5%8C%97%E5%B8%82"
        response = req.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        return soup.select("earthquakeNo")[0]

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.content == '地震' or msg.content == '晃' or msg.content == '搖' or msg.content == '好搖' or msg.content == '好晃':
            await msg.channel.send('@everyone '+ random.choice(earthquake_list)+'  稍後發布最近有感地震報告。\nhttps://www.cwb.gov.tw/V8/C/E/index.html')
            firstNum = earthquake_report.get_earthquake_last_reportNum()
            count = 0
            await asyncio.sleep(60)
            while (count < 16 and earthquake_report.get_earthquake_last_reportNum() == firstNum):
                await asyncio.sleep(15)
                print (count)
                count+=1

            soup = earthquake_report.get_earthquake_soup()

            await msg.channel.send("@everyone\n第 " + str(soup.select("earthquakeNo")[0].text[3:]) + " 號顯著有感地震報告\n\t" + 
            soup.select("reportContent")[0].text + "\n\t\t" + 
            "發震時間 : " + soup.select("originTime")[0].text + "\n\t\t" + 
            "規模 : " + soup.select("magnitudeValue")[0].text + "\n\t\t" +  
            "深度 : " + soup.select("depth value")[0].text + "\n\t\t" + 
            "位置 : " + soup.select("location")[0].text + "\n\t\t" + 
            "警示顏色 : " + soup.select("reportColor")[0].text + "\n\t\t" + 
            soup.select("reportImageURI")[0].text)
            
def setup(bot):
    bot.add_cog(earthquake_report(bot))