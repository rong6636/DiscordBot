"""
2021/07/25
讓機器人報告奧運資訊
"
link >> https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm

"""
from core.classes import Cog_Extension
import discord
from discord.ext import commands


# 引入 requests 模組
import requests
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
# 引入 re 模組
import re
import json
from opencc import OpenCC
from datetime import datetime

# thread時間
import asyncio
import random
import time


class olympic_medal(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ========全域變數區======== #
        
        # ========================= #
        
        # olympic_medal
        def get_olympic_medal():
            cc = OpenCC('s2twp')
            #抓取網頁的連結
            url = "https://olympics.com/tokyo-2020/olympic-games/zh/results/all-sports/medal-standings.htm"
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
            soup = BeautifulSoup(req.text, "html.parser")

            medal = soup.select("#medal-standing")[0]

            team = medal.find_all("tr")[1:]

            medal = {}
            medal["renew_day"] = datetime.now().strftime("%Y-%m-%d")
            for t in team:
                td = t.select("td")
                teamName = cc.convert(td[1].text.strip())
                rank = td[0].text.strip()
                gold = td[2].text.strip()
                silver = td[3].text.strip()
                bronze = td[4].text.strip()
                if teamName == "ROC":
                    teamName = "俄羅斯"
                medal[teamName] = [rank, gold, silver, bronze]
                # print (team, medal[team])
            
            # 取舊的
            with open ('olympics.json', 'r', encoding='utf8') as jfile:
                odata = json.load(jfile)
                jfile.close()
            if odata["中華臺北"][1]+odata["中華臺北"][2]+odata["中華臺北"][3] <= medal["中華臺北"][1]+medal["中華臺北"][2]+medal["中華臺北"][3]:
                with open ('olympics.json', 'w') as f: 
                    json.dump(medal, f, indent=4)
                    f.close()

        # 一切的行為從這裡開始
        async def zha():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                print (">> olympic_medal <<")
                # 取舊的
                with open ('olympics.json', 'r', encoding='utf8') as jfile:
                    odata = json.load(jfile)
                    jfile.close()

                get_olympic_medal()
                # 取新的
                with open ('olympics.json', 'r', encoding='utf8') as jfile:
                    ndata = json.load(jfile)
                    jfile.close()
              

                if odata["中華臺北"][1:] != ndata["中華臺北"][1:]:
                    print(odata["中華臺北"][1:], ndata["中華臺北"][1:])
                    _str = "當前 2020東奧 台灣奧運獎牌更新!\n"
                    _str += "台灣排名: " + str(ndata["中華臺北"][0]) +", \t"+str(ndata["中華臺北"][1]) + "金, " + str(ndata["中華臺北"][2]) + "銀, " + str(ndata["中華臺北"][3]) + "銅"
                    Main_Ch = self.bot.get_channel(603566154153328652)
                    print("str",_str)
                    await Main_Ch.send(_str)

                elif (odata["renew_day"] != datetime.now().strftime("%Y-%m-%d") and datetime.now().strftime("%Y-%m-%d") < "2021-08-08"):
                    print(odata["renew_day"], datetime.now().strftime("%Y-%m-%d"))
                    _str = "當前 2020東京奧運 獎牌榜前十\n"
                    for i in ndata:
                        if i != "renew_day":
                            if int(ndata[i][0])>10:
                                break
                            name = setformatName(i)
                            _str += "\t\t"+ str(ndata[i][0]) + "：\"" +name+"\"\t"
                            _str += str(ndata[i][1]) + "金, " + str(ndata[i][2]) + "銀, " + str(ndata[i][3]) + "銅\n"
                        
                    _str += "==================================\n"
                    _str += "台灣排名: " + str(ndata["中華臺北"][0]) +", \t"+str(ndata["中華臺北"][1]) + "金, " + str(ndata["中華臺北"][2]) + "銀, " + str(ndata["中華臺北"][3]) + "銅"
                    
                    Main_Ch = self.bot.get_channel(603566154153328652)
                    print("str",_str)
                    await Main_Ch.send(_str)
                await asyncio.sleep(7200)
                
        # self.bg_task = self.bot.loop.create_task(zha())

def setformatName(i):
    print("seN")
    _q = ""
    if len(i)<6:
        for q in range(6-len(i)):
            _q+="  "
    return _q+i+_q

def setup(bot):
    bot.add_cog(olympic_medal(bot))