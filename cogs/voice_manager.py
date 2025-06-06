import random
import asyncio
import discord
from discord.ext import commands

class VoiceManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reply_postfix = [
            "登大人", "情勒我", "在玩火", "標準逆子", "純愛戰士", "尊嘟假嘟", "釣鯨魚", "塔綠班", 
            "崩潰仔", "蛋雕", "上鑽了", "山道猴", "急了哦", "很好用", "要確欸",
            "啥款?", "這麼可愛", "硬控我", "貼臉開大", "不洗澡", "是禽獸", "史密斯",
            "命不好","M3?","觸爛","不嘻嘻","吃瓜群眾","有料","歸剛欸","是社畜","干飯人"
            "別墅裡唱K","已讀亂回","不懂就問","讀書犯法","🤡🤡","又贏","還得是你",
        ]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        處理語音狀態更新事件，當成員進入或離開語音頻道時觸發。
        Args:
            member: 成員對象，表示語音狀態更新的成員。
            before: 成員之前的語音狀態。
            after: 成員之後的語音狀態。
        """
        if after.channel is not None and after.channel.id == 678511301881757759:
            print(f"[I] {member.display_name} 打算開啟新語音頻道。")
            guild = self.bot.get_guild(after.channel.guild.id)
            category = self.bot.get_channel(after.channel.category_id)
            room_name = member.display_name + random.choice(self.reply_postfix)
            new_voice_chl = await guild.create_voice_channel(room_name, category=category)
            await member.move_to(new_voice_chl)

        if before.channel is not None and before.channel.category_id == 603566154153328651 and before.channel.id not in [678511301881757759, 603568241612292106]:
            print(f"[I] {member.display_name} 離開了語音頻道 {before.channel.name}。")
            chl = self.bot.get_channel(before.channel.id)
            if len(chl.members) == 0:
                print(f"[I] {member.display_name} 離開了語音頻道 {before.channel.name}，等待三秒準備刪除頻道。")
                for _ in range(3):
                    await asyncio.sleep(3)
                    chl = self.bot.get_channel(before.channel.id)
                    if len(chl.members) != 0:
                        return
                await chl.delete()
async def setup(bot):
    await bot.add_cog(VoiceManager(bot))