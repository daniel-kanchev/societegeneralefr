import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from societegeneralefr.items import Article


class SocietegeneralefrSpider(scrapy.Spider):
    name = 'societegeneralefr'
    start_urls = ['https://particuliers.societegenerale.fr/articles-actualites']

    def parse(self, response):
        links = response.xpath('//a[@class="dcw_card-article_link"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//section[@class="dcw_article-block"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
