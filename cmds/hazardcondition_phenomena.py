"""
2021/07/08
讓機器人報告天氣警特報資訊
天氣特警報 "豪雨" "大豪雨" "超大豪雨"
"
    還未完整測試 需要多次不同的特報發布 才能確定完成
"
opendata link >> https://opendata.cwb.gov.tw/dataset/observation?page=1

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

# thread時間
import asyncio
import random
import time
import rw


class hazardcondition_phenomena(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ========全域變數區======== #
        
        # ========================= #
        
        # 從交通部中央氣象局opendata 取得天氣警特報資料
        def get_hazardconditions_data():
            #抓取網頁的連結, 使用授權碼帳號:信箱justin, 授權碼:CWB-6EA7A397-8B9A-4BE1-BE4D-9A0F69AB0161
            url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization=CWB-6EA7A397-8B9A-4BE1-BE4D-9A0F69AB0161&format=JSON"

            req = requests.get(url)
            reqJSON = req.json()

            if reqJSON["success"] == "true":
                records = reqJSON["records"]
            else:
                records = []
            data = {}
            for record in records["record"]:
                datasetDescription = record["datasetInfo"]["datasetDescription"]
                if datasetDescription != "大雨特報":
                    # location 
                    locationName_list = []
                    for location in record["hazardConditions"]["hazards"]["hazard"]["info"]["affectedAreas"]["location"]:
                        locationName_list.append(location["locationName"])

                    dir_data = {
                        "validTime": record["datasetInfo"]["validTime"]["startTime"] + " ~ " + record["datasetInfo"]["validTime"]["endTime"],
                        "contentText" : record["contents"]["content"]["contentText"],
                        "datasetDescription": datasetDescription,
                        "phenomena": record["hazardConditions"]["hazards"]["hazard"]["info"]["phenomena"],
                        "locationName_list": locationName_list,
                        "startTime": record["datasetInfo"]["validTime"]["startTime"],
                        "endTime": record["datasetInfo"]["validTime"]["endTime"],
                    }
                    data[datasetDescription] = dir_data
            print ("data return test ", data)
            return data

        # 一切的行為從這裡開始
        async def HP_zha():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                rw.check_backup_hazardconditionsState()
                ndata = get_hazardconditions_data()
                odata = rw.r_hazardconditions()
                # 如果新資料與舊資料有一樣的警報 且 舊警報時間還沒過 保留舊的
                for n in ndata:
                    if n in odata and odata[n]["endTime"] > ndata[n]["startTime"]:
                        ndata[n] = odata[n]
                rw.w_hazardconditions(ndata)

                # 過濾已發布過的消息
                for o in odata:
                    if o in ndata and odata[o]["contentText"] == ndata[o]["contentText"]:
                        del ndata[o]

                for d in ndata:
                    Main_Ch = self.bot.get_channel(674136957173104660)
                    await Main_Ch.send("\""+d+"\"\t地區 : " + ", ".join(i for i in ndata[d]["locationName_list"])+"\n"+
                    "\t\t有效時間 : " + ndata[d]["validTime"] +"\n"+
                      "\t\t發布內容 : " + ndata[d]["contentText"])
                rw.backup_hazardconditions_json()
                await asyncio.sleep(3600)
                
        self.bg_task = self.bot.loop.create_task(HP_zha())

            
def setup(bot):
    bot.add_cog(hazardcondition_phenomena(bot))