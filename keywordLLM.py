from imp import reload
import sys
from hanlp_restful import HanLPClient
from textrank4zh import TextRank4Keyword, TextRank4Sentence

class KeywordExtractor:
    def __init__(self):
        pass

    def TR4W(self, text):
        keywords = set()

        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
        except:
            pass
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=text, lower=True, window=2)
        for item in tr4w.get_keywords(20, word_min_len=1):
            keywords.add(item.word)

        return list(keywords)
    
    def HanLP(self, text):
        HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh') # auth不填则匿名，zh中文，mul多语种
        result = HanLP.keyphrase_extraction(text=text, topk=10)
        return result