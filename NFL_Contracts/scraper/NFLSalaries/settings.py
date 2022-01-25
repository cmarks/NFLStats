# -*- coding: utf-8 -*-

# scrapy settings for NFLSalaries project

BOT_NAME = 'NFLSalaries'

SPIDER_MODULES = ['NFLSalaries.spiders']
NEWSPIDER_MODULE = 'NFLSalaries.spiders'

# user-agent
# USER_AGENT = ""

# obey robots.txt rules
ROBOTSTXT_OBEY = True

# configure global database pipelines
DB_SETTINGS = {
    "db": "nfl",
    "user": "postgres",
    "passwd": "",
    "host": "localhost"
}

# configure global item pipelines
ITEM_PIPELINES = {
    'NFLSalaries.yearpipelines.DuplicatesPipeline': 1,
    'NFLSalaries.yearpipelines.DatabasePipeline': 2
}
