"""
    印刷術計畫

    目標：即時性的提供當前世界主要話題。
    當前擷取資源：
    tvbs setv ttv ftv

    1104更新 get_keynews方法 但因需較大記憶體空間 所以目前無法在終端使用

"""

import datetime
import json
import random
from bs4 import BeautifulSoup as soup
import re
import requests
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from ckiptagger import WS, POS, NER
import pandas as pd
import os
import jieba
import jieba.analyse

class NewsCrawler():
    def __init__(self):
        self.session = requests.Session()
        self.LOW_BOUND = 0.08
        self.mode = "jieba"
        
    def get_taiwan_realtime_news(self):
        news = []
        news.extend(self.get_set_news())
        news.extend(self.get_tvbs_news())
        news.extend(self.get_ftv_news())
        news.extend(self.get_ttv_news())
        return news
    
    def get_world_news(self):
        world_news = []
        world_news.extend(self.get_ttv_world_news())
        world_news.extend(self.get_tvbs_world_news())
        return world_news
    
    def get_keynews_with_weight(self, tw_news, wd_news):
        """
        Get keyword-weighted news.
        """
        # Get Taiwan and World news and segment them
        # tw_news = self.get_taiwan_realtime_news()
        # wd_news = self.get_world_news()

        tw_ns = self.segmentation(tw_news)
        wd_ns = self.segmentation(wd_news)

        # Extract keywords based on mode
        if self.mode == "ckiptagger":
            self.tw_keyword = self.zh_tw_extract_keywords(tw_ns)
            self.wd_keyword = self.zh_tw_extract_keywords(wd_ns)
        elif self.mode == "jieba":
            all_news = re.sub("[「」]", "", str(tw_ns + wd_ns))
            self.tw_keyword = self.get_jieba_tags(all_news, 60)
            self.wd_keyword = self.get_jieba_tags(re.sub("[「」]", "", str(wd_ns)), 60)
        else:
            print("Mode not found.")
            return

        # 合併所有新聞並構建新聞字典及其權重
        all_ns = tw_ns + wd_ns
        news_with_weight = {re.sub("[「」]", " ", str(s)): 0 for s in all_ns}

        # Increase weights for news containing keywords and apply penalties for news longer than 8 characters
        for news in news_with_weight:
            for i in self.tw_keyword:
                if i in news:
                    news_with_weight[news] += self.tw_keyword[i]
            for i in self.wd_keyword:
                if i in news:
                    news_with_weight[news] += self.wd_keyword[i] / 2

            if len(news) > 8:
                news_with_weight[news] /= len(news)
                news_with_weight[news] *= 6

            news_with_weight[news] = np.round(news_with_weight[news], 2).astype(float)

        # Filter out news with low weights
        news_with_weight = {i: j for i, j in news_with_weight.items() if j > self.LOW_BOUND}
        return news_with_weight
        
    
    def get_jieba_tags(self, corpus, topK=60):
        _return = {}
        try:
            tags = jieba.analyse.extract_tags(
                str(corpus), 
                topK=topK, 
                withWeight=True, 
                allowPOS=(
                    'n','nr','nr1','nr2','nrj','nrf','ns','nsf','nt','nz','nl','ng',
                    't','tg',
                    's',
                    'v','vd','vn',
                    'a','ad','an','ag','al',
                    'r','rr','rz','rzt','rzs','rzv','ry','ryt','rys','ryv','rg','d', 'eng'
                )
            )
            for t in tags:
                _return[t[0]] = np.round(t[1], 2).astype(float)
        except Exception as e:
            print(f'Error in get_jieba_tags: {e}')
        return _return
        

    def get_keynews(self):
        tw_news = self.get_taiwan_realtime_news()
        wd_news = self.get_world_news()

        tw_ns = self.segmentation(tw_news)
        wd_ns = self.segmentation(wd_news)

        self.tw_keyword = self.zh_tw_extract_keywords(tw_ns)
        self.wd_keyword = self.zh_tw_extract_keywords(wd_ns)

        ns = tw_ns
        ns.extend(wd_ns)

        keyword = self.tw_keyword
        for wdk in self.wd_keyword:
            if wdk not in keyword:
                keyword[wdk] = self.wd_keyword[wdk]
            else:
                keyword[wdk] += self.wd_keyword[wdk]/2

        news_with_weight = {s:0 for s in ns}
        for news in news_with_weight:                               # 依keyword增加權重
            for i in keyword:
                if i in news:
                    news_with_weight[news]+=keyword[i]

            if len(news)>8:                                         # 字數太多 降低權重
                news_with_weight[news]/=len(news)
                news_with_weight[news]*=6                           # 逞罰
            news_with_weight[news] = np.round(news_with_weight[news], 2)
        
        return sorted(news_with_weight.items(), key=lambda x:x[1])

        
#     def zh_tw_extract_keywords(self, corpus, max_df=0.5, min_df=2, use_idf=True, with_verb=True):
#         """繁中關鍵字萃取 運用 CKIPtagger 與 Scikit Learn

#         Reference:
#         https://br19920702.medium.com/%E7%B9%81%E4%B8%AD%E9%97%9C%E9%8D%B5%E5%AD%97%E8%90%83%E5%8F%96-extract-keywords-%E9%81%8B%E7%94%A8-ckiptagger-%E8%88%87-scikit-learn-boom%E5%87%BA%E6%96%B0%E5%97%9E%E5%91%B3-3ec3e681bdec

#         """
#         sw = ['the', 'of', 'is', 'and', 'to', 'in', 'that', 'we', 'for', 'an', 'are', 'by', 'be', 'as', 'on', 'with', 'can', 'if', 'from', 'which', 'you', 'it',  'this', 'then', 'at', 'have', 'all', 'not', 'one', 'has', 'or', 'that', '的', '了', '和', '是', '就', '都', '而', '及', '與', '著', '或', '之', '後', '才', '元', '在', '不', '一個', '沒有', '我們', '你們', '妳們', '他們', '她們', '因此', '因為', '同年', '同時', '唯一', '去年', '原來', '加上', '剩下', '其中', '其他', '不到', '不如', '不止', '不錯', '之外', '不足', '千萬', '如果', '所有', '為了', '若是', '所以', '是否', '於是', '的確', '沒錯', '發現', '公布', '等於', '說法', '表示', '包括']

#         # 文本清理，刪除 "【】"、"《》"、"「」" 等符號
#         collect_corpus = []
#         for i in corpus:
#             clean_c = re.sub('[【】《》「」]', '', i)
#             if len(clean_c) > 0:
#                 collect_corpus.append(clean_c)
        
#         min_df=1
#         collect_corpus = collect_corpus[:10]

#         print ("導入CKIPtagger")
#         # 導入CKIPtagger 斷詞模型
#         ws = WS(r"D:CKIPtagger_data/data")
#         # 執行斷詞
#         word_segment = ws(
#             collect_corpus,
#             sentence_segmentation=True,
#             segment_delimiter_set={'?', '？', '!', '！', '。', ',', '，', ';', ':', '、'})
#         del ws
#         print ("ws pos")

#         # 詞性模型
#         pos = POS(r"D:CKIPtagger_data/data")
#         print ("word_pos")
#         word_pos = pos(word_segment)
#         del pos
#         print ("del pos")


#         # 實體模型
#         ner = NER(r"D:CKIPtagger_data/data")
#         word_entity = ner(word_segment, word_pos)
#         del ner
#         print ("del ner")

#         cut_corpus = []
#         for segment in word_segment:
#             cut_corpus.append(" ".join(segment))

#         vectorizer = TfidfVectorizer(
#             max_df=max_df, 
#             min_df=min_df, 
#             stop_words=sw, 
#             use_idf=use_idf, 
#             token_pattern="(?u)\\b\\w+\\b"
#         )
#         TDIDF_matrix = vectorizer.fit_transform(cut_corpus)

#         df = pd.DataFrame(TDIDF_matrix.T.toarray(), index=vectorizer.vocabulary_.keys())
#         df['SUM'] = df.sum(axis=1)
#         df.sort_values(by=['SUM'], inplace=True)
#         print (f"TDIDF 詞{df.shape[0]}, 句子{df.shape[1]}")


#         entity = set()
#         for ent in word_entity :
#             for it in ent:
#                 if it[2] != "CARDINAL":
#                     entity.add(it[3])
#         print ("entity")

#         ver = set()
#         if with_verb:
#             for i in range(len(word_pos)):
#                 for j in range(len(word_pos[i])):
#                     if word_pos[i][j] in ["VA", "VAC", "VB"] and len(word_segment[i][j])>1 :
#                         ver.add( len(word_segment[i][j]))
#         #                         print (word_segment[i], word_segment[i][j], word_pos[i][j])
#         #     print (f"entity len{len(entity)}, {entity}")
#         print ("ver")

#         keyword = entity.union(ver)
#         keywithweight = {}
#         for r in range(df.shape[0]):
#             if df.iloc[r].name in keyword:
#                 keywithweight[df.iloc[r].name] = df["SUM"].iloc[r]
        
#         return keywithweight
        
    
    def segmentation(self, titles):
        """切句子
        :titles: list[str]
        """
        tmp = []
        for it in titles:
            tmp.extend(re.findall(r"「\S+」|\S{2,}", it))
        return tmp
    
    def get_set_news(self):
        setn_news = set()
        setn_url = "https://www.setn.com/ViewAll.aspx"
        for url in [f"{setn_url}?p={p}" for p in range(1, 3)]:
            req = self.session.get(url)
            newslist = soup(req.text, "html.parser").select("div.newsItems.col-sm-12")
            for i in newslist:
                setn_news.add(i.h3.text)
        return self.clean_titles(setn_news)
        
    def get_tvbs_news(self):
        tvbs_news = set()
        url = "https://news.tvbs.com.tw/realtime"
        req = self.session.get(url)
        newslist = soup(req.text, "html.parser").find_all("h2")
        for i in range (80):
            tvbs_news.add(newslist[i].text)
        return self.clean_titles(tvbs_news)
    
    def get_ftv_news(self):
        ftv_news = set()
        ftv_url = "https://www.ftvnews.com.tw/realtime/"
        for url in [f"{ftv_url}{p}" for p in range(1, 3)]:
            req = self.session.get(url)
            newslist = soup(req.text, "html.parser").find_all("h2")
            for i in newslist:
                ftv_news.add(i.text)
        return self.clean_titles(ftv_news)

    def get_ttv_news(self):
        ttv_news = set()
        ttv_url = "https://news.ttv.com.tw/realtime/"
        for url in [f"{ttv_url}{p}" for p in range(1, 3)]:
            req = self.session.get(url)
            newslist = soup(req.text, "html.parser").select("li div.title")
            for n in newslist:
                ttv_news.add (n.text)
        return self.clean_titles(ttv_news)
    
    def get_ttv_world_news(self):
        ttv_news = set()
        ttv_url = "https://news.ttv.com.tw/category/%E5%9C%8B%E9%9A%9B/"
        for url in [f"{ttv_url}{p}" for p in range(1, 3)]:
            req = self.session.get(url)
            newslist = soup(req.text, "html.parser").select("div.title")
            for n in newslist:
                ttv_news.add (n.text)
        return self.clean_titles(ttv_news)
    
    def get_tvbs_world_news(self):
        tvbs_news = set()
        url = "https://news.tvbs.com.tw/world"
        req = self.session.get(url)
        newslist = soup(req.text, "html.parser").find_all("h2")
        for i in range (60):
            tvbs_news.add(newslist[i].text)
        return self.clean_titles(tvbs_news)
        

    def clean_titles(self, titles):
        """
            清理標題文本
            set儲存處理後的標題
            
        """
        cleaned_titles = set()
        for title in titles:
            title = re.sub(r"(?<=\D)／|／(?=\D)|\\u3000|[?!？|！]|(\.\.\.)", " ", title)
            title = re.sub(r"(\S*)(新聞|直播|快訊|記者|獨家|中職|秒懂|LIVE|Live|live|NEWS|News|news|TTV|TVBS|HD)(\S*)", " ", title)
            cleaned_titles.add(title)
        return cleaned_titles
    
    def save(self, path:str, keynews:dict):
        """
        :param path: json file path
        :param keynews: dict{keynews:wight}
        :return: None
        """
        
        dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        tw_time = dt.astimezone(datetime.timezone(datetime.timedelta(hours=8))) # 轉換時區 -> 東八區
        str_tw_time = tw_time.strftime("%Y/%m/%d %H:%M:%S")

        if os.path.isfile(path) == False:
            data = {
                "lastUpdateTime": "2021/01/01 01:01:01", 
                "keynews": {}
            }
        else:
            with open (path, 'r', encoding='utf8') as jfile:
                data = json.load(jfile)
                jfile.close()
                
        data["lastUpdateTime"] = str_tw_time
        data["keynews"] = keynews

        with open (path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()

    def get_news_from_json(self, path:str):
        """
        :param path: json file path
        :return: news
        """
        if os.path.isfile(path) == False:
            return {}
        with open (path, 'r', encoding='utf8') as jfile:
            data = json.load(jfile)
            jfile.close()
        return data["keynews"]
