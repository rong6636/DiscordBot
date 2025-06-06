'''
    自製RPG模式
    2020/04/26
    第一期:目標把JSON檔格式制定好、能有挖礦動作。
        格式:
            ID:int
            Experience:(Level)int
            CoolDown[]:int
            X:int
            Y:int
            item[]:true false
            cash:int


        格式化:
            js = json.dumps(json.loads(jdata), sort_keys=True, indent=4, separators=(',', ':'))
            複製貼上
    2021/12/02
    久久未更新，喪失目的
'''
import json
import random
import time
import random

import discord
from discord.ext import commands

from core.classes import Cog_Extension

with open ('RPG_Game.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

'''
with open ('RPG_Game.json', 'w', encoding='utf8') as jfile:
    injdata = json.load(jfile)
'''

class RPG_Game(Cog_Extension):

    @commands.command()
    async def rpg(self, ctx, instruction="None", I="None", J="None",Z="None"):
        #檢視玩家狀態 !!!!!!!!!!!!
        with open ('RPG_Game.json', 'r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        
        player = jdata.get(str(ctx.author.id))
        # if instruction=="super":
        #     player[I][J] = Z   
        #     jdata[str(ctx.author.id)] = player
        #     with open ('RPG_Game.json', 'w') as f:#存檔
        #         json.dump(jdata, f)
        #         f.close()
        #     jfile.close()
        
        if player is None:
            await ctx.send(f"{ctx.message.author.mention}"+"unexist")
            await ctx.send("如果要加入遊戲請輸入!rpg create")
        
        elif instruction == "None":
            # 待增加!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print(ctx.author.id)
            # 待增加!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            s1 = "!rpg create               | 創帳號\n"
            s2 = "!rpg cash                 | 查詢錢包\n"
            s3 = "!rpg sell <物資ID> <數量> | 賣物資\n"
            s4 = "!rpg buy <物資ID>         | 買物資\n"
            s5 = "!rpg mine                 | 挖礦"

            await ctx.send(s1+s2+s3+s4+s5)

            jfile.close()
        
        #創建帳號 create !!!!!!!!!!!!
        elif instruction == "create":
            if str(ctx.author.id) in jdata:
                await ctx.send("You had an account!")
                jfile.close()
                return 0
            
            if jdata.get(str(ctx.author.id)) is None:
                jdata["playerNum"] = int(jdata["playerNum"])+1
                newstr = json.dumps({**jdata, **{str(ctx.author.id): jdata["player"]["0000"]}})#新增新的player資料
                json.loads(newstr)
                with open ('RPG_Game.json', 'w') as f: 
                    json.dump(json.loads(newstr), f)
                    f.close()
            
            jfile.close() #先關閉jfile再開啟，重新讀取

            #結束時 提示與檢查
            with open ('RPG_Game.json', 'r', encoding='utf8') as newjfile:
                newjdata = json.load(newjfile)
            #成功Success 失敗Fail
            if newjdata.get(str(ctx.author.id)) is None:
                await ctx.send("Create an account, Fail!")
            else:
                await ctx.send("Create an account, Success!")

            newjfile.close()

        
        #<打獵 hunt> !!!!!!!!!!!!
        elif instruction == "hunt":
            # 增加 施工ING!!!!!!!!!!!!!
            
            #hunt冷卻時間判斷
            print (str(int(player["CoolDown"]["Hunt"])) + ", " + str(int(time.time())))
            if int(player["CoolDown"]["Hunt"]) >= int(time.time()): #還在冷卻時間
                await ctx.send("冷卻時間中，倒數" + str(int(player["CoolDown"]["Hunt"]) - int(time.time())) + "s")
            elif int(player["CoolDown"]["Hunt"]) < int(time.time()):#不在冷卻時間
                player["CoolDown"]["Hunt"] = str(int(time.time()) + 0)  #+CoolDown
                # 隨機掉錢
                # 增加經驗
                # 增加獵物
                print ("ok")
            # 增加 施工ING!!!!!!!!!!!!!

            jfile.close()

        #<挖礦 mine> !!!!!!!!!!!!
        #挖礦 規則:
        #       依照參數算出每次會挖到的物品or礦物
        #所需參數:  r(隨機)
        #       經驗等級
        #       稿力
        #礦物:  
        #   土、沙、安山岩          (level 1鎬力)   3
        #   花崗岩、閃長岩、煤礦    (level 2鎬力)   3
        #   鐵礦、金礦、石英        (level 3鎬力)   3
        #   紅石、青金石            (level 4鎬力)   2
        #   鑽石                    (level 5鎬力)   1
        #   綠寶石、紅寶石、藍寶石   (level 5鎬力,絕對的等級)  3
        #
        #
        elif instruction == "mine":

            if int(player["CoolDown"]["Mine"]) >= int(time.time()): #還在冷卻時間
                await ctx.send("冷卻時間中，倒數" + str(int(player["CoolDown"]["Mine"]) - int(time.time())) + "s")
            elif int(player["CoolDown"]["Mine"]) < int(time.time()):#不在冷卻時間
                player["CoolDown"]["Mine"] = str(int(time.time()) + 5)#+CoolDown
                # player["item"]["0"] = str(int(player["item"]["0"]) + 10)#+土
                
                i = "0" # 增加的物品
                r = 0   # 增加的數量
                if player["item"]["Lv.5_Pickaxe"] == "1":       # Lv.5
                    i = random.choice(['Diamond'])       # 增加的物品
                    r = random.randint(2, 20)       # 增加的數量
                elif player["item"]["Lv.4_Pickaxe"] == "1":     # Lv.4
                    i = random.choice(['Redstone','Lapis'])   # 增加的物品
                    r = random.randint(2, 20)       # 增加的數量
                elif player["item"]["Lv.3_Pickaxe"] == "1":     # Lv.3
                    i = random.choice(['Iron','Gold','Quartz'])# 增加的物品
                    r = random.randint(2, 20)       # 增加的數量
                elif player["item"]["Lv.2_Pickaxe"] == "1":     # Lv.2
                    i = random.choice(['Diorite','Granite','Coal'])# 增加的物品
                    r = random.randint(2, 20)       # 增加的數量
                elif player["item"]["Lv.1_Pickaxe"] == "1":     # Lv.1
                    i = random.choice(['Dirt','Sand','Andesite'])# 增加的物品
                    r = random.randint(2, 20)       # 增加的數量
                else:                                           # 都沒有
                    i = random.choice(['Dirt','Sand'])    # 增加的物品
                    r = random.randint(1, 5)        # 增加的數量
                    
               
                player["item"][i] = str(int(player["item"][i]) + r)
                await ctx.send("此次挖礦收穫 !\n" + "<:Dirt:{}>".format(jdata["EmojiID"]["item"][i]) + jdata["player"]["XXXX"]["item"][i] + ": " + str(r))


                jdata[str(ctx.author.id)] = player
                with open ('RPG_Game.json', 'w') as f:#存檔
                    json.dump(jdata, f)
                    f.close()
            
            jfile.close()

        #販賣物品 Sell !!!!!!!!!!!!
        #販賣 規則:
        #       
        #所需參數:  r(隨機)
        #
        #
        #價格:  
        #   土、沙、安山岩、閃長岩                     0.2 ~ 1.0              10^:0  2^:0
        #   花崗岩、煤礦                                20 ~ 40               10^:1  2^:2
        #   鐵礦、金礦、石英                           800 ~ 1,600            10^:2  2^:4
        #   紅金石、青金石                         128,000 ~ 144,000          10^:3  2^:6
        #   鑽石                                 2,560,000 ~ 3,360,000        10^:4  2^:8
        #   綠寶石、紅寶石、藍寶石            1,024,000,000 ~ 1,344,000,000    10^:5  2^:10
        #
        #
        elif instruction == "sell":
            #確認帳號存在
            if player is None:
                await ctx.send(f"{ctx.message.author.mention}"+"unexist")
                await ctx.send("如果要加入遊戲請輸入!rpg create")
            
                jfile.close()
                return 0

            item = 9999  #輸入物品的ID(預設為:9999)
            if J == "None":  #J預設100
                J = "100"

            if I == "None":  #輸入格式錯誤
                await ctx.send("格式 !rpg sell <物品> 或是 !rpg sell <物品> <數量>")
            elif I == "土" or I == "dirt" or I == "Dirt":                 #賣土!!!
                item = "Dirt"
            elif I == "沙" or I == "Sand" or I == "sand":                 #賣沙!!!
                item = "Sand"
            elif I == "安山岩" or I == "Andesite" or I == "andesite":     #賣安山岩!!!
                item = "Andesite"
            elif I == "閃長岩" or I == "Diorite" or I == "diorite":       #賣閃長岩!!!
                item = "Diorite"
            elif I == "花崗岩" or I == "Granite" or I == "granite":       #賣花崗岩!!!
                item = "Granite"
            elif I == "煤礦" or I == "Coal" or I == "coal":               #賣煤礦!!!
                item = "Coal"
            elif I == "鐵礦" or I == "Iron" or I == "iron":               #賣鐵礦!!!
                item = "Iron"
            elif I == "金礦" or I == "Gold" or I == "gold":               #賣金礦!!!
                item = "Gold"
            elif I == "石英" or I == "Quartz" or I == "quartz":           #賣石英!!!
                item = "Quartz"
            elif I == "紅石" or I == "Redstone" or I == "redstone":       #賣紅石!!!
                item = "Redstone"
            elif I == "青金石" or I == "Lapis" or I == "lapis":           #賣青金石!!!
                item = "Lapis"
            elif I == "鑽石" or I == "Diamond" or I == "diamond":         #賣鑽石!!!
                item = "Diamond"
            elif I == "綠寶石" or I == "Emerald" or I == "emerald":       #賣綠寶石!!!
                item = "Emerald"
            elif I == "紅寶石" or I == "Ruby" or I == "ruby":             #賣紅寶石!!!
                item = "Ruby"
            elif I == "藍寶石" or I == "Aquamarine" or I == "aquamarine": #賣藍寶石!!!
                item = "Aquamarine"
            
            if item != 9999:
                if int(player["item"][str(item)]) < int(J) or int(J) == 0: #販賣數量不足
                    await ctx.send("販賣物品數量不足! " + jdata["player"]["XXXX"]["item"][str(item)] + "剩餘:" + str(player["item"][str(item)]))
                else:                                                      #販賣數量足夠
                    r = 0
                    if item == "Dirt" or item == "Sand" or item == "Andesite" or item == "Diorite" :  #第一階區物品
                        r = random.uniform(0.2, 1.0)
                    elif item == "Granite" or item == "Coal" :                          #第二階區物品
                        r = random.uniform(20, 40)
                    elif item == "Iron" or item == "Gold" or item == "石英" :             #第三階區物品
                        r = random.uniform(800, 1600)
                    elif item == "Redstone" or item == "Lapis" :                         #第四階區物品
                        r = random.uniform(128000, 144000)
                    elif item == "Diamond":                                       #第五階區物品
                        r = random.uniform(2560000, 3360000)
                    elif item == "Emerald" or item == "Ruby" or item == "Aquamarine" :          #第六階區物品
                        r = random.uniform(1024000000, 1344000000)

                    player["item"][str(item)] = int(player["item"][str(item)])-int(J)   #扣掉販賣數量
                    player["Cash"] = int(player["Cash"]) + int(int(J)*r)                #增加金幣
                    await ctx.send("販賣總價格" + str(int(int(J)*r)) + "! " + jdata["player"]["XXXX"]["item"][str(item)] + "剩餘:" + str(player["item"][str(item)]))

            
            jdata[str(ctx.author.id)] = player
            with open ('RPG_Game.json', 'w') as f:#存檔
                json.dump(jdata, f)
                f.close()

            jfile.close()

        #查詢玩家金錢狀況 cash !!!!!!!!!!!!
        elif instruction == "cash":
            await ctx.send(f"{ctx.message.author.mention}" + "Cash :" + str(player["Cash"]))
            jfile.close()


        #開啟商店 Shop !!!!!!!!!!!!
        elif instruction == "shop":
            
            # 增加 施工ING!!!!!!!!!!!!!
            
            # 增加 施工ING!!!!!!!!!!!!!

            jfile.close()

        #購買裝備 Buy !!!!!!!!!!!!
        elif instruction == "buy":

            # 增加 施工ING!!!!!!!!!!!!!
            if I == "None":# 格式錯誤
                await ctx.send("格式: !rpg buy <itemName> or !rpg buy <itemID>")
            elif jdata["Shop"][I] is None:# 輸入錯誤
                await ctx.send("Please check the item name or ID")
            elif int(player["Cash"]) < int(jdata["Shop"][I]):# 付不起 錢不夠
                await ctx.send("YOU can'tafford it.")
            else:
                if I.find("_Pickaxe"):      # 買鎬
                    if player["item"][I] == "1":
                        await ctx.send("已購買過!")
                    elif player["item"]["Lv."+ str(int(I[3])-1) + "_Pickaxe"] == "0":
                        await ctx.send("請先購買前一個等級!")
                    else :
                        player["Cash"] = str(int(player["Cash"]) - int(jdata["Shop"][I]))# 扣掉商品價格
                        player["item"][I] = "1"
                
            jdata[str(ctx.author.id)] = player
            with open ('RPG_Game.json', 'w') as f:#存檔
                json.dump(jdata, f)
                f.close()
            
            # 增加 施工ING!!!!!!!!!!!!!

            jfile.close()

def setup(bot):
    bot.add_cog(RPG_Game(bot))