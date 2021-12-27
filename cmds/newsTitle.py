"""
2020/10/09
讓機器人自動爬蟲去找新聞標題

"""
import asyncio
from datetime import datetime, timedelta, timezone
import json
import os
import random
import re
import rw
import time

import discord
import jieba
import jieba.analyse
import numpy
import requests
from bs4 import BeautifulSoup
from core.classes import Cog_Extension
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class NewsTitle(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del_contain = ['seconds', 'views', 'ago', 'hour', 'minute', 'second', 'queue', 'Add', 'Now', 'playing', 'Streamed',
            '獨家', '曝光', '快訊', '完整公開', '發燒話題', '健康資訊' , '紀錄幕後', 'LIVE', 'Live', '直播', '新聞',
            '三立', '台視', '記者', '嗆', '集', '/', '-' , ','
        ]
        # ============= lee four ============= 
        def get_lee_title(url):
            req = requests.get(url) # 得到網頁原始碼
            if not req:
                print('NewsTitle 李四端的雲端世界 請求失敗')
                return
            titlelist = []
            for title in re.finditer('"text":"(.*?)"', req.text):
                if "李四端的雲端世界" in title.group():
                    temp = title.group()[8:-1].replace("【李四端的雲端世界】", "").replace("－", "").replace("-", "").replace("李四端的雲端世界", "")
                    if len(temp):
                        titlelist.append(temp)
            return titlelist

        def get_lee_titles():
            lee_playlists = []
            lee_titles = []
            playlist_URL = "https://www.youtube.com/c/%E6%9D%8E%E5%9B%9B%E7%AB%AF%E7%9A%84%E9%9B%B2%E7%AB%AF%E4%B8%96%E7%95%8C/playlists"

            req = requests.get(playlist_URL) # 得到網頁原始碼
            if not req:
                print('李四端的雲端世界 請求失敗')
                return

            # 尋找所有"url"後字串，並且找出包含"playlist?list="的清單連結
            for ur in re.finditer('"url":"(.*?)"', req.text):
                if "playlist?list=" in ur.group():
                    lee_playlists.append("https://www.youtube.com" + ur.group()[7:-1])
            # 取得 "主頁前10個 PLAYLIST" 前7個標題
            for playlist in lee_playlists[:7]:
        #         print (playlist)
                lee_titles.extend(get_lee_title(playlist))

            # 取得 "國際政經事-【李四端的雲端世界】PLAYLIST" 前4個標題
            lee_titles.extend(get_lee_title("https://www.youtube.com/playlist?list=PLE2M8k4S4JObW-24qfEiXCqN4jQuM6lUz")[:4])
            return lee_titles

        def get_keywords_from_lee(titles):
            keywords = []
            dictKeyword = {}
            for t in titles:
                dictKeyword.update(dict.fromkeys(get_brackets_content(t), 2)) #「 」內容提取
                keywords.extend(t.split(" "))
            # 整理keyword
            leedel_contain = ['「', '」', '/', '嗆', '集' ]
            temp = []
            for k in keywords:
                flag = True
                for d in leedel_contain:
                    if d in k:
                        flag = False
                if flag and len(k)>2:
                    temp.append(k)
            keywords = list(set(temp))

            dictKeyword.update(dict.fromkeys(keywords, 1))
            return dictKeyword

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # ============= setNEWS ============= 
        def get_setNEWS_titles():
            setNEWS_titles = []
            url = "https://www.youtube.com/c/%E4%B8%89%E7%AB%8BLIVE%E6%96%B0%E8%81%9E/videos"
            req = requests.get(url)
            if not req:
                print('NewsTitle 三立LIVE新聞 請求失敗')
            for title in re.finditer('"label":"(.*?)"', req.text):
                if "三立" in title.group():
                    setNEWS_titles.append(title.group()[9:title.group().find("│")])
        #     print ("\n".join(str(t) for t in setNEWS_titles))
            return setNEWS_titles

        def get_keywords_from_setNEWS(titles):
            keywords = []
            for t in titles:
                keywords.extend(re.split('！|\s', t.replace('\\', '').replace('...', '')))
            temp = []
            for k in keywords:
                flag = True
                for d in del_contain:
                    if d in k:
                        flag = False
                if flag and len(k)>2 and len(k)<10:
                    temp.append(k)

            keywords = list(set(temp))
            return dict.fromkeys(keywords, 1)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # ============= tvbsNEWS ============= 
        def get_tvbsNEWS_titles():
            tvbsNEWS_titles = []
            url = "https://www.youtube.com/c/TVBSNEWS01/videos"
            req = requests.get(url)
            if not req:
                print('NewsTitle TVBSNEWS01 請求失敗')
            for title in list(re.finditer('"text":"(.*?)"', req.text)):
                if "TVBS新聞" in title.group():
                    tvbsNEWS_titles.append(title.group()[8:title.group().find("｜")])
        #     print ("\n".join(str(t) for t in tvbsNEWS_titles))
            return tvbsNEWS_titles

        def get_keywords_from_tvbsNEWS(titles):
            keywords = []
            for t in titles:
                keywords.extend(re.split('！|\s', t.replace('\\', '').replace('...', '')))
            # 整理keyword
            temp = []
            for k in keywords:
                flag = True
                for d in del_contain:
                    if d in k:
                        flag = False
                if flag and len(k)>2 and len(k)<=10:
                    temp.append(k)

            keywords = list(set(temp))
            return dict.fromkeys(keywords, 1)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # ============= ttvNEWS ============= 
        def get_ttvNEWS_titles():
            ttvNEWS_titles = []
            url = "https://www.youtube.com/c/ttvnewsview/videos"
            req = requests.get(url)
            if not req:
                print('NewsTitle ttvnews 請求失敗')
            for title in list(re.finditer('"text":"(.*?)"', req.text))[:70]:
                if len(title.group()[8:-1])>10:
                    ttvNEWS_titles.append(title.group()[8:-1])
        #     print ("\n".join(str(t) for t in ttvNEWS_titles))
            return ttvNEWS_titles

        def get_keywords_from_ttvNEWS(titles):
            keywords = []
            for t in titles:
                keywords.extend(re.split('！|\s|【|】', t.replace('\\', '').replace('...', '')))
            temp = []
            for k in keywords:
                flag = True
                for d in del_contain:
                    if d in k:
                        flag = False
                if flag and len(k)>2 and len(k)<=10:
                    temp.append(k)

            keywords = list(set(temp))
            return dict.fromkeys(keywords, 1)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # ============= keywords_weight ============= 

        def compute_international_keywords_weight(str_data, keywords):
            # 前三十大 標籤
            top30_tags = jieba.analyse.extract_tags(str_data, topK=30, withWeight=True)
            for k in keywords:
                k_index = str_data.find(k) # 抓關鍵字時間位置
                count = 0
                # 與參考字一樣 且 非數字 "質量+1"
                for i in k:
                    for j in str_data:
                        if j == i and not j.isdigit():
                            count += 1
                # 關鍵字含有標籤 乘上權重
                tags_weight = 1
                for t in top30_tags:
                    if t[0] in k:
                        tags_weight+=(t[1]*4)
                count *= tags_weight

                if k_index < len(str_data)/10: # 關鍵字出現時間在前10%
                    count *= 2
                if k_index < len(str_data)/2: # 關鍵字出現時間在前50%
                    count *= 3
                count = int (count/(len(k)/6+0.1)) # 把關鍵字權重比例固定為8個字
                keywords[k] = min(keywords[k]*count, 250)
            return keywords

        def compute_taiwan_keywords_weight(str_data, keywords):
            # 前三十大 標籤
            top30_tags = jieba.analyse.extract_tags(str_data, topK=30, withWeight=True)
            # 前伍十大 標籤
            top50_tags = jieba.analyse.extract_tags(str_data, topK=50, withWeight=True)
            # print ("top30_tags", top30_tags)
            for k in keywords:
                k_index = str_data.find(k) # 抓關鍵字時間位置
                count = 0
                # 與參考字一樣 且 非數字 "質量+1"
                for i in k:
                    for j in str_data:
                        if j == i and not j.isdigit():
                            count += 1
                # 關鍵字含有標籤 乘上權重
                tags_weight = 1
                for t in top30_tags:
                    if t[0] in k:
                        tags_weight+=(t[1]*6)
                for t in top50_tags:
                    if t[0] in k:
                        tags_weight+=(t[1]*3)
                count *= tags_weight

                count = int (count/(len(k)/10+0.1)) # 把關鍵字權重比例固定為8個字
                keywords[k] = keywords[k]*count + int(keywords[k]*count>60)*40 + int(keywords[k]*count>150)*250 # 全重大於150時 在加250!
            return keywords

        def get_brackets_content(_str):
            index_s, index_e = 0, 0
            d_s, d_e = 0, 0
            keyword = ['']
            for i in range(len(_str)):
                if _str[i] == '「':
                    index_s = i
                if _str[i] == '」':
                    index_e = i
                if index_e>index_s:
                    keyword.append(_str[index_s+1:index_e])
                    index_e = 0
            return keyword

        # 取得新的關鍵字
        def get_new_newsKeyword():
            print ("get_new_newsKeyword()")
            # 取得各新聞標題
            lee_keywords = get_keywords_from_lee(get_lee_titles()) # 李四端雲端國際新聞
            setNEWS_keywords = get_keywords_from_setNEWS(get_setNEWS_titles()) # 三立
            tvbsNEWS_keywords = get_keywords_from_tvbsNEWS(get_tvbsNEWS_titles()) # tvbs
            ttvNEWS_keywords = get_keywords_from_ttvNEWS(get_ttvNEWS_titles()) # 台視

            # 擷取各新聞標題關鍵字
            international_newsKeywords, taiwan_newsKeywords = {}, {}
            international_newsKeywords.update(lee_keywords)
            taiwan_newsKeywords.update(setNEWS_keywords)
            taiwan_newsKeywords.update(tvbsNEWS_keywords)
            taiwan_newsKeywords.update(ttvNEWS_keywords)

            # 計算關鍵字權重
            international_newsKeywords = compute_international_keywords_weight(str(international_newsKeywords).replace("！", "").replace("？", ""), international_newsKeywords)
            taiwan_newsKeywords = compute_taiwan_keywords_weight(str(taiwan_newsKeywords).replace("！", "").replace("!", "").replace("？", "").replace("?", ""), taiwan_newsKeywords)
        #     print ('international_newsKeywords:', '\n'.join(str(i)+"："+str(international_newsKeywords[i]) for i in international_newsKeywords), '\n\n')
            # print ('taiwan_newsKeywords:', '\n'.join(str(i)+"："+str(taiwan_newsKeywords[i]) for i in taiwan_newsKeywords), '\n\n')
            
            # 拿取權重超過100的關鍵字
            main_keywords = {}
            for i in international_newsKeywords:
                if international_newsKeywords[i] > 100:
                    main_keywords[i] = international_newsKeywords[i]
            for t in taiwan_newsKeywords:
                if taiwan_newsKeywords[t] >= 100:
                    main_keywords[t] = taiwan_newsKeywords[t]
            return main_keywords


        # ========== 一切的行為從這裡開始 ==========
        async def zha():
            await self.bot.wait_until_ready()
            rw.check_backup_newsKeyword()
            j_keyword = rw.r_newsKeyword()
            self.channel = self.bot.get_channel(int(j_keyword['NewsKeyWordChannel']))
            while not self.bot.is_closed():
                print (">> News keyword <<")
                get_new_newsKeyword()

                twdt = datetime.now(timezone(timedelta(hours=+8))).strftime('%Y/%m/%d %H:%M:%S')
                twdt_sub3H = datetime.now(timezone(timedelta(hours=+5))).strftime('%Y/%m/%d %H:%M:%S')
                # 每三小時 更新關鍵字
                if j_keyword["renewDataTime"] < twdt_sub3H:
                    j_keyword['keywords'] = get_new_newsKeyword()
                    j_keyword["renewDataTime"] = twdt
                    j_keyword['renewLog'].append("NEWS KEYWORDS 已重抓 " + str("----".join(k for k in j_keyword['keywords'])) + " <" + twdt + ">")
                    
                # ___channel名字為新聞標題___
                # 隨機模式
                if j_keyword["NewsKeyWordRandomMode"] == "1":
                    rname = random.choices(list(j_keyword['keywords'].keys()), weights=list(j_keyword['keywords'].values()))[0]
                    await self.channel.edit(name = rname)
                else:
                    sort_keyword = sorted(j_keyword['keywords'].items(), key=lambda x:x[1])
                    await self.channel.edit(name=sort_keyword[-1])
                P_Chal = self.bot.get_channel(int(j_keyword['PrivateChannel']))

                j_keyword['renewLog'].append("NEWS 標題 已更新 " + rname + " <" + twdt + ">")
                # 傳送更新資訊
                if len(j_keyword['renewLog']) > 18:
                    await P_Chal.send("\n".join(str(i) for i in j_keyword['renewLog'])[:1999])
                    j_keyword['renewLog'] = []
                    
                rw.w_newsKeyword(j_keyword)
                await asyncio.sleep(2)
                rw.backup_newsKeyword_json()

                #單位 secand, 86400秒 = 一天
                if j_keyword["NewsKeyWordRandomMode"] == "1":
                    await asyncio.sleep(600)
                else :
                    await asyncio.sleep(86400)

        self.bg_task = self.bot.loop.create_task(zha())
    
def setup(bot):
    bot.add_cog(NewsTitle(bot))
