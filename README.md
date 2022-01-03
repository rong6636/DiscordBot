# 資深工程師

<p align="center">
  <img src="https://user-images.githubusercontent.com/61511627/147499066-f93595a6-6249-4496-8ef4-d479e7c2b77b.png">
</p>
  
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Red-Discordbot">

  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
  <a href="https://discord.com/">
     <img src="https://img.shields.io/discord/603566154153328650" alt="discord channel">
  </a>
</p>

一個基於資料截取、網路架構、任務排程，架設於雲端伺服器的DISCORD生活訊息機器人

## 主要功能

- 每三小時提供新聞關鍵字
- 第一時間提供氣象局地震報告資訊
- 每小時更新天氣警特報資訊
- 與朋友的玩物 - 指令抽圖 :)
- 普通功能：CPC油價、小遊戲、好友呼叫...等
- 有些過時，如：奧林匹克排行...等

隨需求增加，機器人會不斷增加功能。


## 新聞關鍵字
這是我覺得最繁瑣的功能之一，新聞標題來自[Youtube](http://www.youtube.com/)。
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

NEWS keyword： ![image](https://user-images.githubusercontent.com/61511627/147935391-29112d57-313a-4150-a18c-bcd253ecc618.png)  
更新log紀錄  
![image](https://user-images.githubusercontent.com/61511627/147489206-2c7c9e8b-9aa6-4edd-8256-b0aee65acc56.png)   
[CODE](cmds/newsTitle.py)

## 地震報告
- 觸發機器人地震報告功能 >> 機器人回傳報告
- 擷取來自[中央氣象局](https://opendata.cwb.gov.tw/)的地震資訊  
- 整理報告後推播至公眾頻

台灣屬於多地震帶，偶爾的地震發生，人們會互相道平安。機器人若擷取到有關地震的訊息，就執行報告功能，在第一時間告知最新的地震詳細資訊。

![image](https://user-images.githubusercontent.com/61511627/147490389-17de2646-225a-4aa4-8459-079ee4d5b69f.png)   
[CODE](cmds/earthquake_report.py)

## 天氣警特報資訊

- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資訊  
- 提供豪雨、低溫、強風、大霧...等，即時天氣警報訊息。

台灣天氣多變，隨時掌握極端天氣，有助於規劃行程。

![image](https://user-images.githubusercontent.com/61511627/147489909-2425ab93-f447-4f20-b176-89ff0d36811b.png)    
[CODE ](cmds/hazardcondition_phenomena.py)

## 有趣的抽圖
- 照片來自IG爬蟲，存放於雲端
- 特別的是，我還寫了按讚功能，讓倒讚數多的圖片能被系統自動刪掉。

因為自己之前寫了一個IG爬蟲，爬到的圖片很多，但圖片多也沒有人看實在可惜，就順手寫了這個功能。

![image](https://user-images.githubusercontent.com/61511627/147946393-203d6bc2-6151-41b2-9c66-50a8fd73e5c4.png)    
[CODE](cmds/earthquake_report.py)

## 還有很多很多！
- CPC油價  
![image](https://user-images.githubusercontent.com/61511627/147936205-a25a80d6-34e6-4dbb-b446-4987f2545c91.png)
- 2020東奧  
![image](https://user-images.githubusercontent.com/61511627/147936132-ae505603-8363-4227-87e7-d88d48b15ea1.png)
- 小遊戲
- 好友呼叫
- [CMDS](cmds)
- ...


## 為了機器人所使用的服務
- 雲端架設：[![replit](https://camo.githubusercontent.com/5456d62b1dc41ed0e630a0394b751a21439fcb37236fb2afcf871c1385c11d5f/68747470733a2f2f7265706c2e69742f62616467652f6769746875622f616d6972313232362f5265706c742e69742d636f6469676f73)](https://replit.com/)
- 資料回朔問題備份：[jsonstorage](https://app.jsonstorage.net/)

[![](https://img.shields.io/youtube/channel/views/UC3kkchuB6sP0a7rxtF7I2lg?style=social)](https://www.youtube.com/channel/UC3kkchuB6sP0a7rxtF7I2lg)

