# -*- coding: utf-8 -*-

import scrapy

class ProductItem(scrapy.Item):
	launchDate = scrapy.Field()
	title = scrapy.Field()
	pictureUrl = scrapy.Field()
	productUrl = scrapy.Field()

