import scrapy
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from top100bot.items import Stock
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose
import MySQLdb
import MySQLdb.cursors
from scrapy.utils.project import get_project_settings

class StockLoader(ItemLoader):
    #single quota might cause sql error when insert into DB, we just replace it here
    def strip_single_quota(value):
        return value.replace('\'','_')

    def strip_html(value):
        return re.sub('<[^<]+?>', '', value)

    def gen_url(value):
        return "http://stock.finance.sina.com.cn/usstock/quotes/"+str(value)+".html"
    default_output_processor = Compose(lambda v: v[0], unicode.strip, strip_single_quota)
    # This is the output processor, and will overide the default output processor
    url_out = Compose(lambda v: v[0], unicode.strip, gen_url)
    price_out = Compose(lambda v: v[0], unicode.strip, strip_html)
    changed_out = Compose(lambda v: v[0], unicode.strip, strip_html)

class bot(Spider):
    name = "topgainerbot"
    allowed_domains = ["finviz.com"]
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_topgainers",
    ]

    db_truncated_flag = False
    truncate_sql = """truncate table topgainer"""
    pages_crawled = 0

    def truncate_db(self):

        settings = get_project_settings()

        db = MySQLdb.connect(
            host = settings.get('DB_CONNECT')['host'],    # your host, usually localhost
            user= settings.get('DB_CONNECT')['user'],         # your username
            passwd = settings.get('DB_CONNECT')['passwd'],  # your password
            db = settings.get('DB_CONNECT')['db']
        )        # name of the data base
        self.dbpool = db

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        self.cur = db.cursor()
        self.cur.execute(self.truncate_sql)
        self.dbpool.close()

    def parse(self, response):
        if self.db_truncated_flag == False:
            self.truncate_db()
            self.db_truncated_flag = True
        sel = Selector(response)
    	results = sel.xpath('//a[@class="screener-link"]')
    	ticks = sel.xpath('//a[@class="screener-link-primary"]')
        next_url = sel.xpath('//a[b = "next"]/@href')
	    #each row has to be 10 items
        num_stocks = len(ticks)
        for i in range(0,num_stocks):
            stock = StockLoader(item=Stock(), response=response)
            stock.add_value('num',  results[i*10].xpath('text()').extract())
            stock.add_value('ticker', ticks[i].xpath('text()').extract())
            stock.add_value('company', results[i*10+1].xpath('text()').extract())
            stock.add_value('url', ticks[i].xpath('text()').extract())
            stock.add_value('price', results[i*10+7].extract())
            stock.add_value('marketcap', results[i*10+5].xpath('text()').extract())
            stock.add_value('changed', results[i*10+8].extract())
            stock.add_value('volume', results[i*10+9].xpath('text()').extract())
            yield stock.load_item()

        if next_url and self.pages_crawled < 3:
            url = "http://finviz.com/" +str(next_url[0].extract())
            yield scrapy.Request(url, callback=self.parse)

        self.pages_crawled += 1

class toploserbot(bot):
    name = "toploserbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_toplosers",
    ]
    truncate_sql = """truncate table toploser"""


class newhighbot(bot):
    name = "newhighbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_newhigh",
    ]
    truncate_sql = """truncate table newhigh"""

class newlowbot(bot):
    name = "newlowbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_newlow",
    ]
    truncate_sql = """truncate table newlow"""

class overboughtbot(bot):
    name = "overboughtbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_overbought",
    ]
    truncate_sql = """truncate table overbought"""

class oversoldbot(bot):
    name = "oversoldbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_oversold",
    ]
    truncate_sql = """truncate table oversold"""

class unusualvolumebot(bot):
    name = "unusualvolumebot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_unusualvolume",
    ]
    truncate_sql = """truncate table unusualvolume"""

class mostvolatilebot(bot):
    name = "mostvolatilebot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_mostvolatile",
    ]
    truncate_sql = """truncate table mostvolatile"""

class mostactivebot(bot):
    name = "mostactivebot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_mostactive",
    ]
    truncate_sql = """truncate table mostactive"""


class upgradesbot(bot):
    name = "upgradesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=n_upgrades",
    ]
    truncate_sql = """truncate table upgrades"""

class downgradesbot(bot):
    name = "downgradesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=n_downgrades",
    ]
    truncate_sql = """truncate table downgrades"""


