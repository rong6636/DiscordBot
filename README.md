# 資深工程師
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Red-Discordbot">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>

一個基於提供生活訊息運用資料截取、網路架構、任務排程 架設於雲端伺服器的DISCORD機器人

## 主要功能

- 每小時更新天氣警特報資訊
- 每三小時提供新聞關鍵字
- 第一時間提供氣象局地震報告資訊
- 與朋友的玩物 - 指令抽圖 :)
- 普通功能：CPC油價、小遊戲、好友呼叫...。
- 有些過時，如：奧林匹克排行...。

隨需求增加，機器人會不斷增加功能。


## 天氣警特報資訊

- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資料  
- 提供豪雨、低溫、強風...的即時天氣訊息。

![messageImage_1640610508915](https://user-images.githubusercontent.com/61511627/147487490-d343a4e4-4ee3-4de0-9e89-7a8c69f36ae1.jpg)   
[CODE ](cmds/hazardcondition_phenomena.py)

## 新聞關鍵字
這是我覺得最繁瑣的功能之一，新聞標題來自Youtube[]。
#### 爬蟲
- 為盡可能政治中立，擷取多家新聞台，且每個爬蟲都要量身打造。
- 國內來源主要有TVBS、三立、民視與台視。
- 國外來源新聞主要是"李四端的雲端世界"。


#### 關鍵字擷取   
- 先分解個新聞標題，分出有用片段 (#這部分真滴難)。
- 再計算詞彙權重，計算方式採用jieba套件。
- 最後根據出現時間以及次數，計算新聞關鍵字的重要程度。

這個功能花了我最多時間，但也從中學到最多，尤其把爬蟲的底子打扎實不少。
每天看到自己做的機器人，能隨時提供時事資訊，不僅感到快活，也省下不少去看無意義新聞的時間。

![image](https://user-images.githubusercontent.com/61511627/147487316-43557100-cee2-48b8-a5d8-957bab1597b2.png)   
[CODE](cmds/newsTitle.py)

## 地震報告
- 觸發機器人地震報告功能 >> 機器人回傳報告
- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資料  
- 整理報告後推播志公眾頻

![image](https://user-images.githubusercontent.com/61511627/147487372-bf7938e0-5a6d-4b70-b151-f57eba4c6bda.jpg)   
[CODE](cmds/earthquake_report.py)

## 有趣的抽圖
- 照片來自IG爬蟲，存放於雲端
- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資料  
- 整理報告後推播志公眾頻

![messageImage_1640611155457](https://user-images.githubusercontent.com/61511627/147487525-902b2a70-e404-4284-8777-b94eaeefcc17.jpg)
[CODE](cmds/earthquake_report.py)

## 還有很多很多！
- [cmds](cmds)
- CPC油價
- 小遊戲
- 好友呼叫
- 2020東奧
- ...

## 為了機器人所使用的輔助API
- 雲端架設：[replit](https://replit.com/)
- 資料回朔問題備份：[jsonstorage](https://app.jsonstorage.net/)



