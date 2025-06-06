import datetime
import requests
from bs4 import BeautifulSoup
import time
import asyncio
import json
import os
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
import seaborn as sns # 引入Seaborn
import pandas as pd

import configparser
config = configparser.ConfigParser()
config.read('/home/lab705/code/WhaleFishing-BOT_v2/config.ini')


class ApexTask():
    '''
    data form https://github.com/HugoDerave/ApexLegendsAPI and https://apexlegendsapi.com/
    
    main function >> run()
    '''
    def __init__(self):
        self.API_KEY = "uRpURC42yqxM5U22jViw"
        self.ZHA_UID = "1006130161473"

        self.url_club = "https://apexlegendsstatus.com/clubs/69e41597-bb32-41e6-9c50-960f68ef2ca0"
        self.url_basic = "https://api.mozambiquehe.re/bridge?platform=PC&version=5"
        self.url_maprotation = "https://api.mozambiquehe.re/maprotation?version=2" # map api
        
        self.session = requests.Session()
        self.error_list = []
        
    def get_club_members(self):
        """
        取得俱樂部成員與其名稱、UID
        :retype: dict{dict{Name, UID}}
        :return: {UID:{Name, UID}}
        """
        req = self.session.get(self.url_club)
        player_profile = {}
        if req:
            tr = BeautifulSoup(req.text, "html.parser").find_all("tr")
            for i in range(1, len(tr)):
                th = tr[i].find_all("th")
                infor = {
                    "Name":th[0].text.strip(),
                    "UID":th[0].a.get("href")[th[0].a.get("href").find("/PC")+4:-1]
                }
                player_profile[infor["UID"]] = infor
        return player_profile
    
    async def get_user_profile(self, profile:dict):
        """
        取得玩家資訊
        :param profile: 玩家資訊 {Name, UID}
        :return: dict{dict{profile}}
        """
        uid = profile["UID"]
        url = f'{self.url_basic}&uid={uid}&auth={self.API_KEY}'
        print (f'{uid}, {url}')
        reqJson = self.session.get(url).json()
        # reqJson = requests.get('https://api.mozambiquehe.re/bridge?platform=PC&uid=1006130161473&auth=uRpURC42yqxM5U22jViw').json()
        # 中文名 會出錯 但是英文名不會 所以會用到profile
        profile={
            "Name": profile["Name"],
            "UID": profile["UID"],
            "Level":reqJson["global"]["level"],
            "toNextLevelPercent": reqJson["global"]["toNextLevelPercent"],
            "currentLegend":reqJson["legends"]["selected"]["LegendName"],
            "currentLegend_intro":reqJson["legends"]["selected"]["gameInfo"]["intro"],
            "currentLegend_data":reqJson["legends"]["selected"]["data"],
            "currentLegend_icon":reqJson["legends"]["selected"]["ImgAssets"]["icon"],
            "BR_rank": reqJson["global"]["rank"]["rankScore"],
            "BR_rank_name": os.path.basename(reqJson["global"]["rank"]["rankImg"][:-4]),
            "BR_rank_img": reqJson["global"]["rank"]["rankImg"],
            "Arena_rank": reqJson["global"]["arena"]["rankScore"],
            "Arena_rank_img": reqJson["global"]["arena"]["rankImg"],
            "bans": reqJson["global"]["bans"]["remainingSeconds"],
            "isOnline" : reqJson["realtime"]["isOnline"],
            "canJoin" : reqJson["realtime"]["canJoin"],
            "selectedLegend" : reqJson["realtime"]["selectedLegend"],
            "currentStateAsText" : reqJson["realtime"]["currentStateAsText"]
        }
        return profile
    
    def get_map_status(self):
        """
        取得地圖狀態

        :return: dict{map}
        """
        try:
            reqJson = self.session.get(self.url_maprotation+"&auth="+self.API_KEY).json()
            map_status = {
                "battle_royale_current_map": reqJson["battle_royale"]["current"]["map"],
                "battle_royale_current_endTime": reqJson["battle_royale"]["current"]["readableDate_end"],
                "battle_royale_current_mapImg": reqJson["battle_royale"]["current"]["asset"],
                "battle_royale_next_map": reqJson["battle_royale"]["next"]["map"],
                "ranked_current_map": reqJson["ranked"]["current"]["map"],
                "ranked_current_mapImg": reqJson["ranked"]["current"]["asset"],
                "arenasRanked_current_map": reqJson["arenasRanked"]["current"]["map"],
                "arenasRanked_current_mapImg": reqJson["arenasRanked"]["current"]["asset"],
                "arenasRanked_next_map": reqJson["arenasRanked"]["next"]["map"]
            }
        except Exception as e:
            print ("apex get_map_status() ERROR："+str(e))
            return {}
            
        return map_status
    
    def get_log_from_json(self, log_path:str):
        """
        從json檔取得log資料
        """
        if not os.path.isfile(log_path):
            return None
        
        with open (log_path, 'r', encoding='utf8') as jfile:
            log_data = json.load(jfile)
            jfile.close()
        return log_data

    def update_to_json(self, path:str, members_profile:dict, map_status:dict):
        """
        :param path: json file path
        :param members_profile: dict{dict{Name, UID,...}}
        :param map_status: dict{map}
        :return: None
        """
        
        if os.path.isfile(path) == False:
            apex_data = {
                "lastUpdateTime": "2021/01/01 01:01:01", 
                "daily_log":[], 
                "current_map":{}, 
                "apex_color_palette": [
                    "#F20519","#F28322","#F20F79",
                    "#1B20AC","#A030FC","#99D0F2",
                    "#0468BF","#CCA62B","#05C2C7",
                    "#74BF94","#8684BF","#00CC2C",
                    "#BF7373","#F2D8D5"
                ],
            # "apex_fig_path":"/root/WhaleFisher-BOT/apex_rank_daily_log.png"
            }
        else:
            with open (path, 'r', encoding='utf8') as jfile:
                apex_data = json.load(jfile)
                jfile.close()
        dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        tw_time = dt.astimezone(datetime.timezone(datetime.timedelta(hours=8))) # 轉換時區 -> 東八區
        str_tw_time = tw_time.strftime("%Y/%m/%d %H:%M:%S")
        apex_data["lastUpdateTime"] = str_tw_time
        apex_data["daily_log"].append({"time": str_tw_time, "data":members_profile})
        apex_data["current_map"] = map_status

        with open (path, 'w', encoding='utf8') as f:
            json.dump(apex_data, f, indent=4, ensure_ascii=False)
            f.close()
    
    def clear_daily_log(self, path:str):
        """
        清除每日log

        :param path: json file path
        :return: None
        """
        if os.path.isfile(path):
            with open (path, 'r', encoding='utf8') as jfile:
                apex_data = json.load(jfile)
                jfile.close()
            apex_data["daily_log"] = []
            with open (path, 'w', encoding='utf8') as f:
                json.dump(apex_data, f, indent=4, ensure_ascii=False)
                f.close()

    def find_player_with_highest_rank(self, log_list: list):
        """
            從多個log中找最高分數的玩家
            :param log_list: list[dict{uid:dict{}}]
            :return: list[Name, BR_rank]
        """
        name = ""
        BR_rank = 0
        for log in log_list:
            for uid in log:
                if log[uid]["BR_rank"] > BR_rank:
                    name = log[uid]["Name"]
                    BR_rank = log[uid]["BR_rank"]
                    BR_rank_name = log[uid]["BR_rank_name"]
        return [name, BR_rank, BR_rank_name.upper()]
    
    
    def find_player_with_max_jump(self, week_rank_log: list):
        """
            從多個log中找最大跳躍的玩家
            :param week_rank_log: list[dict{uid:dict{}}]
            :return: dict{uid, gap, time1, time2}
        """
        jump = {"uid":"0", "gap":0, "time":""}
        if len(week_rank_log) < 1:
            return jump
        
        for i in range(1, len(week_rank_log)):
            for uid in week_rank_log[i]:
                if uid == "time":
                    continue
                if uid in week_rank_log[i-1]:
                    gap = week_rank_log[i][uid] - week_rank_log[i-1][uid]
                    if gap > jump["gap"]:
                        jump = {"uid":uid, "gap": gap, "time1":week_rank_log[i-1]["time"], "time2":week_rank_log[i]["time"]}
        return jump

    
    def get_uid_name(self, log: dict, uid: str):
        if uid in log:
            return log[uid]["Name"]
        return "Unknown"

    def find_player_with_max_stride(self, a_log: dict, b_log: dict):
        """
        找出在 a_log 和 b_log 中
        進步最多的玩家

        :param a_log: dict{uid:dict{}}
        :param b_log: dict{uid:dict{}}
        :return: list[name, max_stride]
        """
        name = ""
        max_stride = 0

        for uid in a_log:
            if uid in b_log:
                stride = b_log[uid]["BR_rank"] - a_log[uid]["BR_rank"]
                if stride > max_stride:
                    name = b_log[uid]["Name"]
                    max_stride = stride
        return [name, max_stride]
    
    def find_changed_players(self, a_log, b_log):
        """
        找出在 a_log 和 b_log 中
        Name, Level, BR_rank發生變化的玩家

        :param a_log: dict{uid:dict{}}
        :param b_log: dict{uid:dict{}}
        :return: dict{"Name":[], "Level":[], "BR_rank":[]}
        """
        changed_players = {
            "Name":[], "Level":[], "BR_rank":[]
        }

        for uid in b_log:
            if uid in a_log:
                if a_log[uid]["Name"] != b_log[uid]["Name"]:
                    changed_players["Name"].append(uid)
                if a_log[uid]["Level"] != b_log[uid]["Level"]:
                    changed_players["Level"].append(uid)
                if a_log[uid]["BR_rank"] != b_log[uid]["BR_rank"]:
                    changed_players["BR_rank"].append(uid)
        return changed_players
    
    def get_week_rank_log(self, daily_log, rank_players):
        """
        從daily_log中擷取每次log的rank_players的排名變化

        :param daily_log: list{dict{}}
        :param rank_players: list{uid}
        :return: list{dict{}}
        """
        week_rank_log = []
        for i in range(len(daily_log)):
            log_time = datetime.datetime.strptime(daily_log[i]["time"], '%Y/%m/%d %H:%M:%S').strftime('%a %H:%M')
            log = {
                "time":log_time
            }
            for uid in rank_players:
                print (uid)
                if uid in daily_log[i]["data"]:
                    log[uid] = daily_log[i]["data"][uid]["BR_rank"]
            if len(rank_players)>0:
                week_rank_log.append(log)
        return week_rank_log
    
    def drawing_rank(self, log_path:str, save_path:str):
        """
        繪製每週排名變化圖
        :param log_path: json file path
        :param save_path: save path
        :return: None
        """
        if not os.path.isfile(log_path):
            return 
        
        with open (log_path, 'r', encoding='utf8') as jfile:
            apex_data = json.load(jfile)
            jfile.close()

        if apex_data["daily_log"] == []:
            return 

        first_log = apex_data["daily_log"][0]["data"]
        last_log = apex_data["daily_log"][-1]["data"]
        print (last_log)

        changed_players = self.find_changed_players(first_log, last_log)

        #   2)) 擷取RANK變動的玩家
        week_rank_log = self.get_week_rank_log(
            apex_data["daily_log"], changed_players["BR_rank"])
        
        current_highest_rank = self.find_player_with_highest_rank([last_log])
        highest_rank = self.find_player_with_highest_rank([log["data"] for log in apex_data["daily_log"]])
        max_stride = self.find_player_with_max_stride(first_log, last_log)
        max_jump = self.find_player_with_max_jump(week_rank_log)
        print (max_jump)
        
        print ("da 擷取RANK END，時數", len(week_rank_log))
        print (week_rank_log)
        
        #   3)) 做圖表
        if len(week_rank_log)<=0:
            return
        
        df = pd.DataFrame(week_rank_log)
        df.set_index('time', inplace = True)
        ttf_path = config.get('server', 'path')+'/TaipeiSansTCBeta-Regular.ttf'
        FontProperties_1 = FontProperties(fname=ttf_path, size=10) # 這裡請寫上自己的ttf路徑
        FontProperties_2 = FontProperties(fname=ttf_path, size=20) # 這裡請寫上自己的ttf路徑
        FontProperties_3 = FontProperties(fname=ttf_path, size=30) # 這裡請寫上自己的ttf路徑

        fontManager.addfont(ttf_path)
        mpl.rc('font', family='Taipei Sans TC Beta')

        plt.rcParams['figure.facecolor'] = 'black'
        plt.rcParams['axes.facecolor'] = '#1d1f27'
        plt.rcParams['axes.titlecolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['font.size'] = '12'
        apex_color_palette = apex_data["apex_color_palette"]
        colors = sns.color_palette(apex_color_palette, len(df.columns))
        fig = plt.figure(figsize=(15,10))
        # rank
        # add_axes( x初始座標, y初始座標, 寬, 高 )
        rank = fig.add_axes([0.07, 0.27, 0.85, 0.6])
        rank.set_prop_cycle(color=colors)
        for i in df:
            name = apex_data["daily_log"][-1]["data"][i]["Name"]
            print (f'i = {i}, "{name}"')
            rank.plot(df[i], linewidth=2, label=name)
        rank.legend(prop=FontProperties_1, labelcolor='w', loc='lower left')
        rank.set_title("本周APEX RANK玩家", fontproperties = FontProperties_3, loc ='left')
        rank.set_xlabel("TIME", c='w')
        rank.set_ylabel("SCORE", c='w')
        rank.xaxis.set_tick_params(rotation = 50)

        logo = fig.add_axes([0.45, 0.92, 0.1, 0.07])
        logo.axis('off')

        textblock = fig.add_axes([0.1, 0.05, 0.8, 0.2])
        textblock.axis('off')
        textblock.text(0, 0.50, f"當前最高分："+current_highest_rank[0]+"    {:,} RP ".format(current_highest_rank[1])+" "+current_highest_rank[2], fontproperties = FontProperties_1, color="w", fontsize=15)
        textblock.text(0, 0.35, f"本周歷史最高：{highest_rank[0]}", fontproperties = FontProperties_1, color="w", fontsize=15)
        textblock.text(0, 0.20, f"本周爬分最多：{max_stride[0]}", fontproperties = FontProperties_1, color="w", fontsize=15)
        textblock.text(0, 0.05, f"本周爆發最強：{self.get_uid_name(last_log, max_jump['uid'])},    {max_jump['time1']}-{max_jump['time2']} 加分分數：{max_jump['gap']}", fontproperties = FontProperties_1, color="w", fontsize=15)
        fig.savefig(save_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300, bbox_inches='tight', pad_inches=0.1)
        print ("apex fig end.")
        pass