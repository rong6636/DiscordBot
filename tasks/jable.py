import re
import time

import requests
from bs4 import BeautifulSoup

class JableCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }

    def sort_jable_list(self, jable_list):
        def _calculate_score(av):
            view = av["view"]
            like = av["like"]
            score = ((like / view) * 100) ** 2 * (view // 100000)
            return score
        
        sorted_list = sorted(
            jable_list, 
            key=_calculate_score,
            reverse=True
        )
        return sorted_list
    
    def break_string(self, text):
        pattern = r"(?<=.{20})[.,?!。？！～」 …]"
        match = re.search(pattern, text[:35])
        if match:
            return text[:match.start() + 1]
        else:
            return text[:25]+'…'

    def formatted_title_list(self, jable_list):
        return [self.break_string(jable["title"]) for jable in jable_list]
        
    def get_jable_latest_list(self, mode="latest_updates", pages=5):
        assert mode in ["latest_updates", "new_release"], "mode must be 'latest_updates' or 'new_release'"
        
        param = '?mode=async&function=get_block&block_id=list_videos_latest_videos_list&sort_by='
        if mode == "new_release":
            url = f"https://fs1.app/{mode}/{param}release_year&from="
        if mode == "latest_updates":
            url = f"https://fs1.app/{mode}/{param}post_date&from="
        
        jable = []
        for p in range(1, pages+1):
            time.sleep(1)
            content = self.session.get(url+str(p), timeout=20).text
            soup = BeautifulSoup(content, "html.parser")
            details = soup.find_all('div', class_='detail')
            
            for detail in details:
                h6 = detail.find('h6', class_='title').text

                p_element = detail.find('p', class_='sub-title')
                text = p_element.get_text().replace(' ', '')
                view, like = re.findall(r'\d+', text)[:2]
                jable.append({
                    "car":h6.split()[0], 
                    "title":h6, 
                    "view":int(view), 
                    "like":int(like)
                })
        return jable
    
    def get_jable_category_list(self, category=1, sort_mode=0, pages=5):
        category_list = [
            "chinese-subtitle", "pantyhose", "rape", "roleplay", "groupsex", "uniform", "pov", "sex-only",
        ]
        sort_mode_list = [
            "most_favourited", "video_viewed", "post_date", "post_date_and_popularity"
        ]
        
        category = category_list[category]
        sort_mode = sort_mode_list[sort_mode]
        
        # https://fs1.app/categories/chinese-subtitle/?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=most_favourited
        url = f"https://fs1.app/categories/{category}/?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by={sort_mode}"
        req = self.session.get(url, timeout=20)
        
        jable = []
        if not req:
            print (f'ERROR: jable {url} {req}')
            return jable
        
        content = req.text
        soup = BeautifulSoup(content, "html.parser")
        details = soup.find_all('div', class_='detail')
        for detail in details:
            h6 = detail.find('h6', class_='title').text
            p_element = detail.find('p', class_='sub-title')
            text = p_element.get_text().replace(' ', '')
            view, like = re.findall(r'\d+', text)[:2]
            jable.append({
                "car":h6.split()[0], 
                "title":h6, 
                "view":int(view), 
                "like":int(like)
            })
        print (f'jable {jable}')
        return jable