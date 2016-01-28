import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from top100bot.items import Stock, FdaStock
import scrapy.loader
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
import MySQLdb
import MySQLdb.cursors
from scrapy.utils.project import get_project_settings
import re

def clean_db(table_name, category):
    settings = get_project_settings()
    db = MySQLdb.connect(
        host = settings.get('DB_CONNECT')['host'],    # your host, usually localhost
        user= settings.get('DB_CONNECT')['user'],         # your username
        passwd = settings.get('DB_CONNECT')['passwd'],  # your password
        db = settings.get('DB_CONNECT')['db']
    )
    # name of the data base
    dbpool = db

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    clean_db_sql = r"delete from "+table_name+" where `category` = " + r"'" + category + r"'"
    cur.execute(clean_db_sql)
    dbpool.close()

def add_stock_defaults(stock):
    stock.add_value('num', 'null')
    stock.add_value('ticker', 'null')
    stock.add_value('company', 'null')
    stock.add_value('url', 'null')
    stock.add_value('price', 'null')
    stock.add_value('volume', 'null')
    stock.add_value('category', 'null')
    stock.add_value('sector', 'null')
    stock.add_value('industry', 'null')
    stock.add_value('country', 'null')
    stock.add_value('marketcap', 'null')
    stock.add_value('pe', 'null')
    stock.add_value('change', 'null')
    stock.add_value('exchange', 'null')
    stock.add_value('trades', 'null')
    stock.add_value('shortint', 'null')
    stock.add_value('float', 'null')
    stock.add_value('outstd', 'null')
    return stock


class StockLoader(ItemLoader):
    #single quota might cause sql error when insert into DB, we just replace it here
    def strip_single_quota(value):
        return value.replace('\'','_')

    def strip_html(value):
        return re.sub('<[^<]+?>', '', value)

    def gen_url(value):
        return "http://stock.finance.sina.com.cn/usstock/quotes/"+str(value)+".html"
    default_output_processor = Compose(lambda v: v[0], strip_single_quota)
    # This is the output processor, and will overide the default output processor
    url_out = Compose(lambda v: v[0], gen_url)
    price_out = Compose(lambda v: v[0], strip_html)
    change_out = Compose(lambda v: v[0], strip_html)
    pe_out = Compose(lambda v: v[0], strip_html)
    category_out = Compose(lambda v: v[0])
    num_out = Compose(lambda v: v[0])


class FdaStockLoader(ItemLoader):
    def strip_single_quota(value):
        return value.replace('\'','_')
    default_output_processor = Compose(lambda v: v[0], strip_single_quota)


class fdacalendartsbot(Spider):
    name = "fdacalendarsbot"
    start_urls = [
        "http://www.biopharmcatalyst.com/fda-calendar/",
    ]

    def parse(self, response):
        # reset the db
        clean_db('stockdata_fdastock', 'fda')
        sel = Selector(response)
        results = sel.xpath('//table[@class = "sortable"]/tbody/tr')
        num_stocks = len(results)
        for i in range(0, num_stocks): # the first row is title
            html = results.extract()[i]
            match = re.search(r'<tr><td><a.*?>(.*?)</a></td>.*?<td.*?>(.*?)</td><td.*?>(.*?)</td>.*?<td>(.*?)</td><td.*?>(.*?)</td>.*?<td><a.*?href="(.*?)".*?>(.*?)</a></td></tr>', html, re.S)
            if match:
                fdaStock = FdaStockLoader(item=FdaStock(), response=response)
                fdaStock.add_value('ticker', match.group(1).encode("utf-8"))
                fdaStock.add_value('price', match.group(2).encode("utf-8"))
                fdaStock.add_value('marketcap', match.group(3).encode("utf-8"))
                fdaStock.add_value('phasetype',match.group(4).encode("utf-8"))
                fdaStock.add_value('duedate' ,match.group(5).encode("utf-8"))
                fdaStock.add_value('details_link', match.group(6).encode("utf-8"))
                #fdaStock.add_value('details', match.group(7).encode("utf-8")) # encoding error, TODO FIX
                fdaStock.add_value('details', 'details')
                url = r"http://stock.finance.sina.com.cn/usstock/quotes/"+str(match.group(1).encode("utf-8"))+r".html"
                fdaStock.add_value('url', url)
                fdaStock.add_value('category', 'fda')
                fdaStock.add_value('volume','') # no use
                yield fdaStock.load_item()

class shortintsbot(Spider):
    name = "shortintsbot"
    #myurl = "http://www.highshortinterest.com/all/1"
    category = 'shortints'
    start_urls = []
    base_url = "http://www.highshortinterest.com/all/"

    page_id = 1
    db_cleaned_flag = False

    def __init__(self, category='', myurl=None, base_url=None):
        self.category = category
        self.start_urls = [myurl,]
        self.base_url = base_url

    def parse(self, response):
        if self.db_cleaned_flag == False:
            clean_db('stockdata_stock', self.category)
            self.db_cleaned_flag = True

        sel = Selector(response)
        results = sel.xpath('//table[@class = "stocks"]/tr')

        num_stocks = len(results)
        for i in range(1,num_stocks): # the first row is title
            stock = StockLoader(item=Stock(), response=response)
            stock = add_stock_defaults(stock)
            stock.replace_value('category', self.category)
            html = results.extract()[i]
            match = re.search(r'<tr><td><a.*?>(.*?)</a></td>.*?<td>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>\n<td.*?>(.+?)</td>.+?<td.*?>(.+?)</td>.*?<td>(.*?)</td>.*?</tr>', html, re.S)
            if match:
                stock.replace_value('num', str(i+(self.page_id-1)*50))
                stock.replace_value('ticker', match.group(1).encode("utf-8"))
                stock.replace_value('company', match.group(2).encode("utf-8"))
                stock.replace_value('exchange', match.group(3).encode("utf-8"))
                if self.name == 'shortintsbot':
                    stock.replace_value('shortint', match.group(4).encode("utf-8"))
                    stock.replace_value('float', match.group(5).encode("utf-8"))
                    stock.replace_value('outstd', match.group(6).encode("utf-8"))
                else:
                    stock.replace_value('float', match.group(4).encode("utf-8"))
                    stock.replace_value('outstd', match.group(5).encode("utf-8"))
                    stock.replace_value('shortint', match.group(6).encode("utf-8"))
                stock.replace_value('industry', match.group(7).encode("utf-8"))
                stock.replace_value('url', match.group(1).encode("utf-8"))
                yield stock.load_item()

        if  self.page_id < 6:
            self.page_id += 1
            url = self.base_url +str(self.page_id)
            yield scrapy.Request(url, callback=self.parse)

class stockbot(Spider):
    name = "topgainersbot"
    category = ''
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_topgainers",
    ]

    db_cleaned_flag = False
    pages_crawled = 0

    def __init__(self, category='', myurl=None):
        self.category = category
        self.start_urls = [myurl,]

    def parse(self, response):
        if self.db_cleaned_flag == False:
            clean_db('stockdata_stock', self.category)
            self.db_cleaned_flag = True
            ##print("cleaned db")
        sel = Selector(response)
        next_url = sel.xpath('//a[b = "next"]/@href')
        results = sel.xpath('//tr[@class="table-dark-row-cp"]') #dark rows
        results.extend(sel.xpath('//tr[@class="table-light-row-cp"]')) # light rows

        num_stocks = len(results)
        #print("num stock%d"%num_stocks)

        for i in range(0,num_stocks):
            #print("i %d"%i)
            stock = StockLoader(item=Stock(), response=response)
            stock = add_stock_defaults(stock)
            stock.replace_value('category', self.category)
            html = results.extract()[i]
            #print html
            match = re.search(r'<tr.*?>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?><a.*?>(.*?)</a></td>.*?', html, re.S)
            if match:
                #print match.groups()
                stock.replace_value('num', match.group(1).encode("utf-8"))
                stock.replace_value('ticker', match.group(2).encode("utf-8"))
                stock.replace_value('company', match.group(3).encode("utf-8"))
                stock.replace_value('sector', match.group(4).encode("utf-8"))
                stock.replace_value('industry', match.group(5).encode("utf-8"))
                stock.replace_value('country', match.group(6).encode("utf-8"))
                stock.replace_value('marketcap', match.group(7).encode("utf-8"))
                stock.replace_value('pe', match.group(8).encode("utf-8"))
                stock.replace_value('price', match.group(9).encode("utf-8"))
                stock.replace_value('change', match.group(10).encode("utf-8"))
                stock.replace_value('volume', match.group(11).encode("utf-8"))
                stock.replace_value('ticker', match.group(2).encode("utf-8"))
                stock.replace_value('url', match.group(2).encode("utf-8"))
                yield stock.load_item()


        if next_url and self.pages_crawled < 3:
            url = "http://finviz.com/" +str(next_url[0].extract())
            #print url
            self.pages_crawled += 1
            yield scrapy.Request(url, callback=self.parse)


'''
class toplosersbot(stockbot):
    name = "toplosersbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_toplosers",
    ]


class newhighsbot(stockbot):
    name = "newhighsbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_newhigh",
    ]

class newlowsbot(stockbot):
    name = "newlowsbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_newlow",
    ]

class overboughtsbot(stockbot):
    name = "overboughtsbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_overbought",
    ]

class oversoldsbot(stockbot):
    name = "oversoldsbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_oversold",
    ]

class unusualvolumesbot(stockbot):
    name = "unusualvolumesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_unusualvolume",
    ]

class mostvolatilesbot(stockbot):
    name = "mostvolatilesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_mostvolatile",
    ]

class mostactivesbot(stockbot):
    name = "mostactivesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=ta_mostactive",
    ]


class upgradesbot(stockbot):
    name = "upgradesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=n_upgrades",
    ]

class downgradesbot(stockbot):
    name = "downgradesbot"
    start_urls = [
        "http://finviz.com/screener.ashx?v=110&s=n_downgrades",
    ]

class lowfloatsbot(shortintsbot):
    name = "lowfloatsbot"
    category = "lowfloats"
    start_urls = [
        "http://www.lowfloat.com/all/1",
    ]
    base_url = "http://www.lowfloat.com/all/"

'''