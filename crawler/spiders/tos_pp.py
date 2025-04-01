import scrapy  
from bs4 import BeautifulSoup  

class TosPpSpider(scrapy.Spider):  
    name = "tos_pp"  
    start_urls = [
    "https://www.apple.com/legal/privacy/",
    "https://policies.google.com/terms"
]
    def parse(self, response):  
        soup = BeautifulSoup(response.text, 'html.parser')  
        text = ' '.join([p.get_text() for p in soup.find_all('p')])  
        yield {  
            'url': response.url,  
            'text': text[:10000]  # First 10k chars  
        }  