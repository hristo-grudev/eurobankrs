import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import EurobankrsItem
from itemloaders.processors import TakeFirst


class EurobankrsSpider(scrapy.Spider):
	name = 'eurobankrs'
	start_urls = ['https://www.eurobank.rs/about-us/novosti.53.html']

	def parse(self, response):
		post_links = response.xpath('//h4[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if response.url[-3:] == 'pdf':
			return
		title = response.xpath('//div[@class="block"]/h1/text()').get()
		description = response.xpath('//div[@class="block"]//text()[normalize-space() and not(ancestor::h4 | ancestor::p[@class="datum"])]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="block"]/p[@class="datum"]/text()').get()

		item = ItemLoader(item=EurobankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
