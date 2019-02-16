import pip
pip.main(["install", "Scrapy”])
s = ''
import scrapy
import logging

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        logging.info("here "+str(next_page))
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            ‘''
with open("quote_spider.py", 'w') as f:
    f.write(s)

import scrapy
from scrapy.utils.markup import remove_tags
import re
import logging
base_url = 'http://www.lokmat.com/latestnews/page/%d'
ptrn = re.compile('\xa0+')

class LokmatSpider(scrapy.Spider):
    name = 'lokmat'
    start_urls = [base_url%(i) for i in range(0,45000)]
    

    def parse(self, response):
        # follow links next pages
        self.logger.info(response.request.url)
        next_pages = response.css('a[class=red]::attr(href)')
        if len(next_pages) > 0:
            for href in next_pages:
                yield response.follow(href.extract(), self.parse_news)

    def parse_news(self, response):   
        complete_news = response.css('.article-content p::text')
        complete_news = ' '.join([n.extract() for n in complete_news])
        complete_news = remove_tags(complete_news)
        complete_news = ptrn.sub(' ', complete_news)        
        yield {
            'url': response.request.url,
            'title': response.css('.article-description::text').extract_first(),
            'news': complete_news
        }


import scrapy
from scrapy.utils.markup import remove_tags
import re
import logging

ptrn = re.compile('\xa0+')
urls_list = list()
genre_list = ['maharashtra', 'desh-videsh', 'krida', 'manoranjan', 'mumbai', 'thane', 'navimumbai', 'pune', 'nagpur', 'nashik', 'aurangabad', 'kolhapur' ]
genre_size = [1169, 1723, 844, 844, 1636, 538, 150, 843, 194, 159, 111, 74]
list_size = len(genre_list)

base_url = 'https://www.loksatta.com/trending/more/%s/%d/24/'
for i in range(0,list_size):
    for j in range(2,genre_size[i]+1):
        urls_list.append(base_url%(genre_list[i],j))
        
print("Length URLs :", len(urls_list))
class LoksattaSpider(scrapy.Spider):
    name = 'loksatta'
    start_urls = urls_list
    

    def parse(self, response):
        # follow links next pages
        self.logger.info(response.request.url)
        next_pages = response.css('a::attr(href)')
        if len(next_pages) > 0:
            for href in next_pages:
                yield response.follow(href.extract(), self.parse_news)

    def parse_news(self, response):      
        complete_news = response.css('p+ p , #rightsec p:nth-child(1)::text')
        complete_news = ' '.join([n.extract() for n in complete_news])
        complete_news = remove_tags(complete_news)
        complete_news = ptrn.sub(' ', complete_news)        
        yield {
            'url': response.request.url,
            'title': response.css('#headline::text').extract_first(),
            'news': complete_news
        }