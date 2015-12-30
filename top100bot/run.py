from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('topgainerbot')
process.crawl('toploserbot')
process.crawl('newhighbot')
process.crawl('newlowbot')
process.crawl('unusualvolumebot')
process.crawl('overboughtbot')
process.crawl('oversoldbot')
process.crawl('mostvolatilebot')
process.crawl('mostactivebot')
process.crawl('upgradesbot')
process.crawl('downgradesbot')

process.start()
print("done.....")