from collections import Counter  
import sqlite3  
import json  

class SQLitePipeline:  
    def open_spider(self, spider):  
        self.conn = sqlite3.connect("tos_pp.db")  
        self.cur = self.conn.cursor()  
        self.cur.execute("""CREATE TABLE IF NOT EXISTS documents  
                          (url TEXT, text TEXT, word_freq TEXT)""")  # Added word_freq column  

    def process_item(self, item, spider):  
        # Calculate word frequencies  
        words = item['text'].split()  
        word_freq = dict(Counter(words).most_common(20))  

        # Store everything  
        self.cur.execute("INSERT INTO documents VALUES (?, ?, ?)",  
                        (item["url"], item["text"], json.dumps(word_freq)))  
        self.conn.commit()  
        return item  

    def close_spider(self, spider):  
        self.conn.close()  
from textblob import TextBlob  

class SentimentPipeline:  
    def process_item(self, item, spider):  
        analysis = TextBlob(item["text"])  
        item["sentiment"] = {  
            "polarity": round(analysis.sentiment.polarity, 2),  # -1 (negative) to 1 (positive)  
            "subjectivity": round(analysis.sentiment.subjectivity, 2)  # 0 (factual) to 1 (opinionated)  
        }  
        return item  