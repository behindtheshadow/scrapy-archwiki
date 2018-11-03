# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy_archwiki.items import ArchwikiCategoryItem
from scrapy_archwiki.items import ArchwikiPageItem


class ContentSpider(scrapy.Spider):
    name = 'content'
    start_urls = ['https://wiki.archlinux.org/index.php/Table_of_contents']

    def parse(self, response):
        tds = response.css("#mw-content-text table td")
        for td in tds:
            for a in td.css("a"):
                yield response.follow(a, callback=self.parse_mw_pages)

    def parse_mw_pages(self, response):
        category = ItemLoader(item=ArchwikiCategoryItem(), response=response)
        
        category.add_css('category', '#firstHeading::text')
        category.add_css('pages', '#mw-pages .mw-content-ltr li ::text')
        category.add_css('sub_category', '#mw-subcategories .mw-content-ltr li a ::attr(title)')
        category.add_css('parent_category', '#mw-normal-catlinks li a::attr(title)')
        yield category.load_item()

        mw_pages = response.css("#mw-pages .mw-content-ltr")
        pages = mw_pages.css("li")
        for page in pages:
            item = ItemLoader(ArchwikiPageItem(), page)
            item.add_css('title', 'a::attr(title)')
            item.add_css('url', 'a::attr(href)')
            yield item.load_item()
