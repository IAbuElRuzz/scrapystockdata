from scrapy.item import Item, Field


class Stock(Item):
    num = Field()
    ticker = Field()
    company= Field()
    url = Field()
    price = Field()
    marketcap = Field()
    changed = Field()
    volume = Field()



