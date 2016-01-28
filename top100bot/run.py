from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time




class crawl_tasks(object):

    list_5min = ['topgainersbot', 'toplosersbot', 'unusualvolumesbot']
    list_1hour = ['toplosersbot', 'unusualvolumesbot',
              'topgainersbot','newhighsbot', 'newlowsbot',
              'overboughtsbot', 'oversoldsbot',
              'mostvolatilesbot', 'mostactivesbot',
              'upgradesbot', 'downgradesbot']

    clist = []

    list_all = ['fdacalendarsbot','toplosersbot', 'unusualvolumesbot',
              'topgainersbot','newhighsbot', 'newlowsbot',
              'overboughtsbot', 'oversoldsbot',
              'mostvolatilesbot', 'mostactivesbot',
              'upgradesbot', 'downgradesbot', 'lowfloatsbot', 'shortintsbot']


    def __init__(self, flag):
        if flag == '5min':
            self.clist = self.list_5min
        elif flag == '1hour':
            self.clist = self.list_1hour
        else:
            self.clist = self.list_all


    def crawl_tasks(self):
        process_all = CrawlerProcess(get_project_settings())
        for c in self.clist:
            process_all.crawl(c)

        process_all.start()



if __name__ == '__main__':
    c = crawl_tasks('all')
    c.crawl_tasks()
    #process_all = CrawlerProcess(get_project_settings())
    #process_all.crawl('fdacalendarsbot')
    #process_all.start()

if __name__ == '__lolo__':
    tcount = 0

    while True:
        print("===============================================")
        print("======")
        print("Start crawl task")
        print("======")
        print("===============================================")

        if tcount%12 == 0:
            print("===============================================")
            print("======")
            print("Start crawl task on 1 hour: %d"%(tcount%12))
            print("======")
            print("===============================================")
            c = crawl_tasks('1hour')
        else:
            print("===============================================")
            print("======")
            print("Start crawl task on 5 min: %d"%tcount)
            print("======")
            print("===============================================")
            c = crawl_tasks('5min')

        c.crawl_tasks()
        del c

        tcount += 1
        time.sleep(5*60)
