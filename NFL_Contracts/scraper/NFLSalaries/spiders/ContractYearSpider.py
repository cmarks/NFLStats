from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.spiders import Spider
from w3lib.html import remove_tags
from ..items import ContractYear

class ContractYearSpider(Spider):
    name = 'contract_year_spider'
    start_urls = ['https://overthecap.com/position/']
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         'NFLSalaries.yearpipelines.DuplicatesPipeline': 1,
    #         'NFLSalaries.yearpipelines.DatabasePipeline': 2
    #         }
    #     }

    def parse(self, response):
        years = response.css("#select-year > option::attr(value)").extract()
        years = [str(i) for i in range(1984, 2032)]
        for position_slug in response.css("#select-position > option::attr(value)").extract():
            for year in years:
                url = self.start_urls[0] + position_slug + "/" + year
                yield Request(url, callback=self.extract, meta={"position": position_slug, "year": year})

    def extract(self, response):
        for row in response.css(".position-table > tbody > tr"):
            item_loader = ItemLoader(item=ContractYear(), selector=row)
            # removes html tags
            item_loader.default_input_processor = MapCompose(remove_tags)
            item_loader.default_output_processor = TakeFirst()

            item_loader.add_css("player", "td:nth-of-type(1)")
            item_loader.add_css("team", "td:nth-of-type(2)")
            item_loader.add_css("cap_number", "td:nth-of-type(3)")
            item_loader.add_css("cash_spent", "td:nth-of-type(4)")
            item_loader.add_value("position", response.meta["position"])
            item_loader.add_value("year", response.meta["year"])
            yield item_loader.load_item()
