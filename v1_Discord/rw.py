# read and write json file

import json
import os
import time
import requests
from datetime import datetime, timedelta, timezone



# hazardconditions JSON檔
def r_hazardconditions():
    check_JSONExist('hazardconditions.json', data={"BackupTime": "2021/01/01 01:01:01"})
    with open ('hazardconditions.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)
        jfile.close()
    return jdata

# 寫入hazardconditions JSON檔
def w_hazardconditions(jdata):
    with open ('hazardconditions.json', 'w', encoding='utf8') as f: 
        json.dump(jdata, f, indent=4)
        f.close()

# newsKeyword JSON檔
def r_newsKeyword():
    check_JSONExist('newsKeyword.json', data={"BackupTime": "2021/01/01 01:01:01", "renewDataTime": "2021/01/01 01:01:01", "keywords":{}, 'renewLog':[]})
    with open ('newsKeyword.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)
        jfile.close()
    return jdata

# 寫入newsKeyword JSON檔
def w_newsKeyword(jdata):
    with open ('newsKeyword.json', 'w', encoding='utf8') as f: 
        json.dump(jdata, f, indent=4)
        f.close()


# setting JSON檔
def r_setting():
    with open ('setting.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)
        jfile.close()
    return jdata

# 寫入 setting JSON檔
def w_setting(jdata):
    with open ('setting.json', 'w', encoding='utf8') as f: 
        json.dump(jdata, f, indent=4)
        f.close()

# ==============================================
#  =========       BACKUP AREA       ========== 
# ==============================================

# 備份 app.jsonstorage hazardconditions
def backup_hazardconditions_json():
    j_hazardconditions = r_hazardconditions()
    twdt = datetime.now(timezone(timedelta(hours=+8))).strftime("%Y/%m/%d %H:%M:%S") # 備份時間
    j_hazardconditions["BackupTime"] = twdt

    req = requests.put("https://api.jsonstorage.net/v1/json/1fbb6c99-1bf6-4eb7-82d0-de8346fc224c?apiKey=82132140-94c3-4e8e-890c-794d7d0b8dd0", json = j_hazardconditions)
    if req:
        w_hazardconditions(j_hazardconditions)
        print ("BackUp hazardconditions Success in " + twdt)
    else:
        print("hazardconditionsState"+str(req))

# check 備份 app.jsonstorage hazardconditionsState
def check_backup_hazardconditionsState():
    j_hazardconditions = r_hazardconditions()
    req = requests.get("https://api.jsonstorage.net/v1/json/1fbb6c99-1bf6-4eb7-82d0-de8346fc224c")
    if req:
        backupHazardconditions = req.json()
        if j_hazardconditions["BackupTime"] < backupHazardconditions["BackupTime"]:
            w_hazardconditions(backupHazardconditions)
    print ("end check hd")

# 備份 app.jsonstorage newsKeyword
def backup_newsKeyword_json():
    j_newsKeyword = r_newsKeyword()
    twdt = datetime.now(timezone(timedelta(hours=+8))).strftime("%Y/%m/%d %H:%M:%S") # 備份時間
    j_newsKeyword["BackupTime"] = twdt

    req = requests.put("https://api.jsonstorage.net/v1/json/19a99d5a-4dee-41b6-a5d4-468fa0a1a116?apiKey=82132140-94c3-4e8e-890c-794d7d0b8dd0", json = j_newsKeyword)
    if req:
        w_newsKeyword(j_newsKeyword)
        print ("BackUp newsKeyword Success in " + twdt)
    else:
        print("newsKeywordState"+str(req))

# check 備份 app.jsonstorage newsKeyword
def check_backup_newsKeyword():
    j_newsKeyword = r_newsKeyword()
    req = requests.get("https://api.jsonstorage.net/v1/json/19a99d5a-4dee-41b6-a5d4-468fa0a1a116")
    if req:
        backupNewsKeyword = req.json()
        if j_newsKeyword["BackupTime"] < backupNewsKeyword["BackupTime"]:
            w_newsKeyword(backupNewsKeyword)

# 備份 app.jsonstorage setting
def backup_setting_json():
    j_setting = r_setting()
    twdt = datetime.now(timezone(timedelta(hours=+8))).strftime("%Y/%m/%d %H:%M:%S") # 備份時間
    j_setting["BackupTime"] = twdt

    req = requests.put("https://api.jsonstorage.net/v1/json/6d120211-7bcb-4b6e-85af-10dbf3a0fd1f/83018bed-b488-498c-bf55-98e8a406c0f5?apiKey=82132140-94c3-4e8e-890c-794d7d0b8dd0", json = j_setting)
    if req:
        w_setting(j_setting)
        print ("BackUp setting Success in " + twdt)
    else:
        print("setting"+str(req))

# check 備份 app.jsonstorage newsKeyword
def check_backup_setting():
    j_setting = r_setting()
    req = requests.get("https://api.jsonstorage.net/v1/json/6d120211-7bcb-4b6e-85af-10dbf3a0fd1f/83018bed-b488-498c-bf55-98e8a406c0f5")
    
    if req:
        backupSetting = req.json()
        if j_setting["BackupTime"] < backupSetting["BackupTime"]:
            w_setting(backupSetting)
    

# 備份到 app.jsonstorage
def backup_jsonData():
    backup_hazardconditions_json()

# check 備份 app.jsonstorage
def check_backup():
    check_backup_hazardconditionsState()
# ^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=

# 確認資料存在
def check_JSONExist(filepath, data = {}):
    if os.path.isfile(filepath) == False:
        with open (filepath, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4)
            f.close()
