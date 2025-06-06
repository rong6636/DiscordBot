import time
import re
import json
import os
import requests
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import imageio
from PIL import Image

class TaiPower:
    def __init__(self, root_path=None):
        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        self.root_path = root_path

    def get_each_energy_capacity(self):
        """
        Get device generating capacity
        :return: every type generating capacity
        """
        energy_capacity = {}
        
        url = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
        content = self.session.get(url, timeout=20).json()
        aaData = content['aaData']
        
        pattern = r"<A NAME='([^']*)'></A><b>[^()]*\("
        pattern2 = r'(\d+\.\d+)\((\d+\.\d+%)\)'
        pattern3 = r'#\S*|[amp;]|\(\S+\)'
        pattern4 = r'-|N/A'

        energy_capacity = {}

        for i in range(len(aaData)):
            power_type = re.search(pattern, aaData[i][0]).group(1)
            unit = re.sub(pattern3, '', aaData[i][2])

            if power_type not in energy_capacity:
                energy_capacity[power_type] = {}

            if unit == "小計":
                device_capacity = re.search(pattern2, aaData[i][3])
                net_generation = re.search(pattern2, aaData[i][4])

                energy_capacity[power_type]["小計"] = {
                    "device_capacity": float(device_capacity.group(1)), 
                    "device_capacity_rate": device_capacity.group(2), 
                    "net_generation": float(net_generation.group(1)), 
                    "net_generation_rate": net_generation.group(2)
                }

            else:
                if unit not in energy_capacity[power_type]:
                    energy_capacity[power_type][unit] = {
                        "device_capacity": 0,
                        "net_generation": 0
                    }
                cap = float(re.sub(pattern4, '0', aaData[i][3]))
                gener = float(re.sub(pattern4, '0', aaData[i][4]))
                energy_capacity[power_type][unit]["device_capacity"] += cap
                energy_capacity[power_type][unit]["net_generation"] += gener
                
        return energy_capacity
    
    def get_current_power_info(self):
        """
        Get power info
        :return: power info
        """
        url = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.json"
        content = self.session.get(url, timeout=20).json()
        
        return {
            "curr_load" : float(content["records"][0]["curr_load"]),
            "curr_max_sply_capacity" : float(content["records"][3]["real_hr_maxi_sply_capacity"]),
            "daily_max_sply_capacity" : float(content["records"][1]["fore_maxi_sply_capacity"]),
            "pred_daily_peak_load": float(content["records"][1]["fore_peak_dema_load"]),
            "pred_daily_peak_range": content["records"][1]["fore_peak_hour_range"],
            "publish_time": content["records"][1]["publish_time"],
        }
    
    def save(self, log_path, power_info, energy_capacity):
        """
        Save data to json file
        :param path: path of json file
        :param power_info: power info
        :param energy_capacity: every energy type generating capacity

        """
        
        if os.path.isfile(log_path) == False:
            data = {}
        else:
            with open (log_path, 'r', encoding='utf8') as jfile:
                data = json.load(jfile)
                jfile.close()
                
        data[power_info["publish_time"]] = {
            "power_info":power_info,
            "energy_capacity":energy_capacity 
        }
        
        with open (log_path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()

    def get_gif_weekly_energy_pie(self, log_path, save_path):
        """
        Get gif of weekly energy pie
        :param log_path: path of json file
        :param save_path: path of gif file

        """

        with open(log_path, 'r') as file:
            data = json.load(file)
        # 取得最一週的時間戳
        weekly_timestamp = list (data.keys())[-3*24*7:]
        # weekly_timestamp = list (data.keys())[-3*7:]
        for i, timestamp in enumerate(weekly_timestamp):
            energy = {}
            for energy_type, plants in data[timestamp]["energy_capacity"].items():
                if "小計" not in plants:
                    continue
                energy[energy_type] = plants["小計"]['net_generation']

            save_dir_path = os.path.join(self.root_path, "energy_pie")
            if not os.path.isdir(save_dir_path):
                os.makedirs(save_dir_path)
            self.draw_energy_pie(energy, timestamp, f"{save_dir_path}/{i}.png")
    
        # 生成gif
        # 創建一個空的圖片列表
        images = []

        # 讀取每個圖片並添加到圖片列表中
        for idx in range(len(os.listdir(save_dir_path))):
            image_path = os.path.join(save_dir_path, f'{idx}.png')
            print (image_path)
            if not os.path.isfile(image_path):
                continue
            img = Image.open(image_path)
            images.append(img)

        # 保存圖片列表為GIF動畫
        imageio.mimsave(save_path, images, duration=0.15)  # 設定每幀的顯示時間

        print(f'GIF已經保存為 {save_path}')
        
    def draw_energy_pie(self, energy_data, timestamp, save_path=None):
        """
        Draw energy pie
        :param energy_data: every energy type generating capacity
        :param timestamp: timestamp
        :param save_path: path of image file

        
        TODO:   1. 每日發電量
                2. 每日發電佔比
                3. 每日發電量趨勢


        """
        color_table = {
            "nuclear": "#F0BA32",
            "coal": "#717056",
            "ippcoal": "#919046",
            "cogen": "#99E643",
            "lng": "#4E70E6",
            "ipplng": "#6E90EE",
            "oil": "#59488E",
            "diesel": "#393AE6",
            "hydro": "#00E6D7",
            "wind": "#92E5D8",
            "solar": "#E6E322",
            "pumpinggen": "#33E6D7",
            "pumpingload": "#55E6D7",
            "OtherRenewableEnergy": "#858595",
        }
        # type, generation, color
        energy_type = []
        energy_generation = []
        energy_color = []
        tatal = sum(energy_data.values())
        for e_type in energy_data:
            if energy_data[e_type]/tatal > 0.02:
                energy_type.append (e_type)
                energy_generation.append (energy_data[e_type])
                energy_color.append (color_table[e_type])
        # 設定中文字型
        font = FontProperties(fname=f"{self.root_path}/TaipeiSansTCBeta-Regular.ttf", size=14)
        plt.close('all')

        fig = plt.figure()
        # 背景顏色
        hour = int(timestamp[-5:-3])
        fig.set_facecolor(self.get_sky_color(hour))
        # 繪製圓餅圖
        plt.pie(energy_generation, labels=energy_type, autopct="%1.1f%%", colors=energy_color, textprops={'fontproperties': font})
        # 設定圖形屬性
        plt.axis("equal")
        plt.title(f"{timestamp}發電佔比", fontproperties=font)
        # plt.show()
        if save_path:
            plt.savefig(save_path)

    def get_sky_color(self, hour):
        # 定义颜色映射，可以根据需要进行自定义
        color_mapping = {
            0: "2C407A",     # 
            4: "2C407A",     # 
            7: "ADEDF7",     # 
            14: "E6FCED",    # 
            16: "FFF1A2",    # 
            20: "2C407A",    # 
            24: "2C407A"     # 
        }

        # 查找最接近的较低和较高的小时，用于插值颜色
        lower_hour = max(key for key in color_mapping.keys() if key <= hour)
        higher_hour = min(key for key in color_mapping.keys() if key > hour)

        # 如果找到完全匹配的小时，返回相应颜色
        if hour in color_mapping:
            return f'#{color_mapping[hour]}'

        # 否则，进行线性插值以获取中间颜色
        lower_color = color_mapping[lower_hour]
        higher_color = color_mapping[higher_hour]

        # 线性插值计算颜色
        interpolation_factor = (hour - lower_hour) / (higher_hour - lower_hour)
        r = int((1 - interpolation_factor) * int(lower_color[0:2], 16) + interpolation_factor * int(higher_color[0:2], 16))
        g = int((1 - interpolation_factor) * int(lower_color[2:4], 16) + interpolation_factor * int(higher_color[2:4], 16))
        b = int((1 - interpolation_factor) * int(lower_color[4:6], 16) + interpolation_factor * int(higher_color[4:6], 16))

        # 将RGB值转换为十六进制颜色表示
        interpolated_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return interpolated_color
