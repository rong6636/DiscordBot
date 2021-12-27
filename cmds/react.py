"""
功能: 
    抽圖

"""

import asyncio
import json
import os
import random
import discord
from core.classes import Cog_Extension
from discord.ext import commands

with open ('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


replyByePhotoList = [
    " 與你...那曾經...",
    " 稍縱即逝...",
    " 你稍微一放鬆就...",
    " 不感興趣的，讓他過去",
    " 不喜歡的，很快就會消失",
    " 民主社會，我們一致通過刪除這些",
    " 票多的贏，票少的...這位...",
    " 以追其所見....",
    " 那該死的小粉紅nmsl",
    " 這些東西，用過就丟...",
    " 她將被我們遺忘...",
]

replyListPre = [
    "辣個男人 ","嘿嘿~ ", "阿斯~ ","喔哇! ","巨根 " ,"魔鬼 " ,"八尺 " ,
    "巨大 ", "吸我懶趴辣 ", "舔 ","絕頂 " ,"解禁 " ,"肉便 " ,
    "汁男 " , "厚厚精華 " ,"樣貌清純 " ,"鬼畜 " ,"霸根 " ,"香 ", 
    "Maid " ,"Outdoor ", "Bestiality ","Blonde " ,"Triple Penetration " ,
    "Hairless " ,"Ladyboy " ,"Chikan " ,"Bunny Girl ","老人小孩都愛用 !",
    " 來嗑CocAiNA", "抽~", "尻尻尻尻", "@%#$!@$&**#", " 深度 !", " 哪位?", 
    " 客有吹洞蕭者"," 綠煙紅霧，彌漫二十餘里"," 歌吹為風，粉汗為雨",
]
replyListPost = [
    " 停車坐愛楓林晚", " 青、取之於藍，而青於藍",
    " 靖共爾位，好是正直。", " 是以各以所長，相輕所短", " 家有弊帚，享之千金",
    " 若有作姦犯科，及為忠善者", " 不宜偏私， 使內外異法也", " 本布衣，躬於紅袂",
    " 今當遠離，臨表涕泣，不知所云", " 君往東廂，任意選之",
    " 中無雜樹，芳草鮮美，落英繽紛", "  卿未可言，待我思之",
    " 吾本乘興而去，興盡而返，何必見戴？", " 高臺未傾，愛妾尚在",
    " 傾壼而醉", " 非吾所謂傳其道、解其惑者也"," 聖人之所以為聖",
    " 愚人之所以為愚", " 古之聖人，其出人也遠矣"," 朝暉夕陰，氣象萬千",
    " 波瀾不驚，上下天光，一碧萬頃", " 岸芷汀蘭，郁郁青青", " 醉翁之意不在酒",
    " 先天下之憂而憂，後天下之樂而樂"," 風霜高潔，水落而石出者",
    " 巧笑知堪敵萬機，傾城最在著戎衣", " 太守醉也"," 太守宴也"," 釀泉為酒，泉香而酒洌",
    " 宴酣之樂，非絲非竹，射者中，弈者勝"," 前者呼，後者硬"," 禽鳥知山林之樂",
    " 望美人兮天一方", " 羽化而登仙", " 一日之盛，為朝煙，為夕嵐",

]
replyList = [
    "娉娉裊裊十三餘，荳蔻梢頭二月初", "嫻靜猶如花照水，行動好比風扶柳",
    "翠眉蟬鬢生別離，一望不見心斷絕", "花心定有何人捻，暈暈如嬌靨",
    "落魄江湖載酒行，楚腰纖細掌中輕", "回眸一笑百媚生，六宮粉黛無顏色",
    "黃鶯不語東風起，深閉朱門伴細腰", "一枝紅艷露凝香，雲雨巫山枉斷腸",
    "金鞭爭道寶釵落，何人先入光明宮", "楊家有女初長成，養在深閨人未識",
    "芙蓉不及美人妝，水殿風來珠翠香", "燭明香暗畫樓深，滿鬢清霜殘雪思難任",
    "態濃意遠淑且真，肌理細膩骨肉勻", "憑闌半日獨無言，依舊竹聲新月似當年",
    "俏麗若三春之桃，清素若九秋之菊", "共道幽香聞十里，絕知芳譽亘千鄉",
    "眉梢眼角藏秀氣，聲音笑貌露溫柔", "衣帶漸寬終不悔，為伊消得人憔悴",
    "冰肌自是生來瘦，那更分飛後", "秀靨艷比花嬌，玉顏艷比春「紅」",
    "千秋無絕色，悅目是佳人", "裊娜少女羞，歲月無憂愁",
    "鳴箏金粟柱，素手玉房前", "柳腰春風過，百鳥隨香走",
    "秀色掩今古，荷花羞玉顏", "絕代有佳人，幽居在空谷",
    "美人既醉，朱顏酡些", "驀然回首，亭亭玉立",
]

class React(Cog_Extension):
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == int(jdata['PicChannel']):
            print("----------")
            print(payload.member, end = ' ')
            
            PIC_CHANNEL = self.bot.get_channel(int(jdata['PicChannel']))
            data = await self.bot.http.get_message(int(jdata['PicChannel']), payload.message_id)
            
            #幹你老師找超九 Data是一維list，裡面放所有message所有資訊
            #然後要找的'filename' 在這個LIST的'attachments'裡面
            #所以要把'attachments'提出來後在找'filename'在第幾個
            
            #print(data)
            #print(data.keys())
            #print("----------")
            #print(data['attachments'])
            #photoid >> 找出照片ID
            a = str(data['attachments'])
            fi = a.find("'filename': ")
            fi2 = a.find(".jpg'")
            photoid = int(a[fi+13:fi2])
            print(photoid)

            #print("----------")
            # cul >> 算出讚差距
            a = str(data['reactions'])
            e = a.find("'name': '👍'")
            e2 = a.find(", 'me': True}, {'")
            ee = a.find("'name': '👎'")
            ee2 = a.find(", 'me': True}]")
            cul = int(a[e+22:e2]) - int(a[ee+22:ee2])
            print(payload.emoji, end = ' ')
            print(str(cul))

            # 如果小於-2
            if cul <= -2:
                msg = await PIC_CHANNEL.fetch_message(payload.message_id)
                await msg.delete()
                
                oldP = jdata['Pic'] + str(int(photoid/40)) + '/' + str(photoid) + '.jpg'
                newP = 'SEXY_IMG_PLAN_B/' + str(os.listdir('SEXY_IMG_PLAN_B')[-1])
                # remove被投票掉的檔案
                os.remove(oldP)
                # 把備用照片 改名 改位置
                os.rename( newP, oldP)
                print("Change Photo:" + newP + " >> " + oldP)
                await PIC_CHANNEL.send(random.choice(replyByePhotoList))
                
            print("----------")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        elif '抽' in ctx.content or ctx.content == "!img":
            await ctx.delete()
            rp = random.randint(0,int(jdata['PicMax']))

            pic = discord.File(jdata['Pic'] + str(int(rp/40)) + '/' + str(rp) +'.jpg')
            print (pic)
            PIC_CHANNEL = self.bot.get_channel(int(jdata['PicChannel']))

            r = random.randint(0, 50)
            name = f"{ctx.author.mention}"

            R = random.randint(1,3)
            if R == 1:
                msg = await PIC_CHANNEL.send(random.choice(replyListPre) + name + " !" , file = pic)
            elif R == 2 :
                msg = await PIC_CHANNEL.send(name + random.choice(replyListPost), file = pic)
            else:
                msg = await PIC_CHANNEL.send(random.choice(replyList), file = pic)
            #msg = await PIC_CHANNEL.send(file = pic)
            #await PIC_CHANNEL.send("😂")
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        
        elif ctx.channel.id == int(jdata['PicChannel']):
            print("DE")
            await asyncio.sleep(3600)
            await ctx.delete()
        
    
def setup(bot):
    bot.add_cog(React(bot))
