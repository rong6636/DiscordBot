# 資深工程師
一個基於提供生活訊息運用資料截取、網路架構、任務排程 架設於雲端伺服器的DISCORD機器人

[![Discord](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
AngularJS-powered HTML5 Markdown editor.


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

[CODE](cmds/newsTitle.py)

## 地震報告
- 觸發機器人地震報告功能 >> 機器人回傳報告
- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資料  
- 整理報告後推播志公眾頻

[CODE](cmds/earthquake_report.py)

## 有趣的抽圖
- 照片來自IG爬蟲，存放於雲端
- 使用[中央氣象局](https://opendata.cwb.gov.tw/)的天氣警特報資料  
- 整理報告後推播志公眾頻

[CODE](cmds/earthquake_report.py)

## 還有很多很多！
- [cmds](cmds)
- CPC油價
- 小遊戲
- 好友呼叫
- 2020東奧
- ...

## 為了機器人所使用的輔助API
- 伺服器架設：[replit](https://replit.com/)
- 伺服器回朔處理：[jsonstorage](https://app.jsonstorage.net/)



