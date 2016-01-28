from scrapy.item import Item, Field


# for topgainers, toplosers etc
class Stock(Item):
    num = Field(default='null')
    ticker = Field(default='null')
    company= Field(default='null')
    url = Field(default='null')
    price = Field(default='null')
    volume = Field(default='null')
    category = Field(default='null')
    sector = Field(default='null')
    industry = Field(default='null')
    country = Field(default='null')
    marketcap = Field(default='null')
    pe = Field(default='null')
    change = Field(default='null')
    exchange = Field(default='null')
    trades = Field(default='null')
    shortint = Field(default='null')
    float = Field(default='null')
    outstd = Field(default='null')

class FdaStock(Item):
    ticker = Field(default='null')
    marketcap= Field(default='null')
    url = Field(default='null')
    price = Field(default='null')
    volume = Field(default='null')
    phasetype = Field(default='null')
    duedate = Field(default='null')
    details = Field(default='null')
    details_link = Field(default='null')
    category = Field(default='null')

