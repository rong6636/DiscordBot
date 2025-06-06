from bs4 import BeautifulSoup
import requests


class LoLVersionChecker():
    def __init__(self):
        self.session = requests.Session()
        self.updates_url = "https://www.leagueoflegends.com/zh-tw/news/game-updates/"
        
    def get_new_version_info(self, previous_titles):
        req = self.session.get(self.updates_url)
        req.encoding = "utf-8"
        if not req:
            return f'ERROR：LOL 版本資訊 {self.updates_url} 請求失敗'
        
        versionNews = BeautifulSoup(req.text, "html.parser").select(".style__Wrapper-sc-1h41bzo-0")
        version_info_list = []
        
        for news in versionNews:
            title = news.select_one(".style__Title-sc-1h41bzo-8").text
            if "版本更新" not in title:
                continue
            if title not in previous_titles:
                url = "https://www.leagueoflegends.com" + news.get('href')
                req = self.session.get(url)
                req.encoding = "utf-8"
                if not req:
                    return f'ERROR：LOL 版本資訊 title:{title}, {self.updates_url} 請求失敗'
                
                versionContainer = BeautifulSoup(req.text, "html.parser").select_one("#patch-notes-container")
                
                version_info_list.append({
                    "title": title,
                    "info": versionContainer.select_one(".blockquote").text,
                    "url": url,
                    "banner_img": news.select_one(".style__ImageWrapper-sc-1h41bzo-5").img.get("src"),
                    "content_img": [img.get("src") for img in versionContainer.find_all("img") if "1920x1080" in img.get("src")],
                    "riot_logo" : "https://images.contentstack.io/v3/assets/blt2ac872571a60ee02/blt68e0c49c61c177a8/61786ce57569022433507c15/RIOT_PairedLogo_White_650px.png",
                    "LOL_logo" : "https://images.contentstack.io/v3/assets/blt2ac872571a60ee02/blt13808f30c8f50340/6172dbbffd37c069473b06f5/leage-of-legends-full-logo.png"
                })
        return version_info_list