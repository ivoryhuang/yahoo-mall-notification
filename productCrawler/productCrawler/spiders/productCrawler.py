from productCrawler.items import ProductItem
import scrapy
import json
import re
import os
from time import sleep
import datetime

dirPath = os.path.dirname(os.path.dirname(__file__))

class ProductSpider(scrapy.Spider):

	name = 'product'

	with open('{}/config/crawler.json'.format(dirPath)) as file:
		crawlerConfig = json.load(file)

	allowed_domains = crawlerConfig['allowed_domains']
	start_urls = crawlerConfig['start_urls']

	def __init__(self):

		self.isNewArrivalEnd = False
		self.urls = {}

		with open('{}/config/shop.json'.format(dirPath)) as file:
			shopConfig = json.load(file)['shops']

		for shop in shopConfig:
			shopSID = shop['sid']

			self.urls[shopSID] = []

			for url in self.crawlerConfig['listAllItmesByLaunchTimeUrls']:
				self.urls[shopSID].append(url.format(sid=shopSID))

	def parse(self, response):

		for shopSID, urls in self.urls.items():

			self.isNewArrivalEnd = False

			for url in urls:
				sleep(1)
				yield scrapy.Request(url, callback=self.parseProduct)
				if self.isNewArrivalEnd:
					break

	def parseProduct(self, response):
		
		item = ProductItem()

		productRows = response.css('tbody')[len(response.css('tbody'))-1].css('tr')

		for productRow in productRows:

			try:
				pic = productRow.css('th[class=pic]')
				
				if not pic:
					continue

				launchDateString = productRow.xpath('following-sibling::tr')[0].css('td[class=nlastd]')[0].extract()
				launchDate = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", launchDateString).group(0)
				todayDate = datetime.date.today().strftime('%Y-%m-%d')

				if launchDate != todayDate:
					self.isNewArrivalEnd = True
					return
				
				item['launchDate'] = launchDate
				item['title'] = productRow.css('img::attr(alt)')[0].extract()
				item['pictureUrl'] = productRow.css('img::attr(style)')[0].extract().replace("background-image:url('", '').replace("');", '')
				item['productUrl'] = productRow.css('a::attr(href)')[0].extract()
				yield item

			except Exception as e:
				print(str(e))
		



