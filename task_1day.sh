#! /bin/sh    
export PATH=$PATH:/usr/local/bin
cd /Users/ethanzhang/PycharmProjects/top100bot

scrapy crawl shortintsbot -a myurl="http://www.lowfloat.com/all/1" -a base_url="http://www.lowfloat.com/all/" -a category=lowfloats &
scrapy crawl shortintsbot -a myurl="http://www.highshortinterest.com/all/1" -a base_url="http://www.highshortinterest.com/all/" -a category=shortints &
scrapy crawl fdacalendarsbot &
scrapy crawl topgainersbot -a category=upgrades -a myurl="http://finviz.com/screener.ashx?v=110&s=n_upgrades" &
scrapy crawl topgainersbot -a category=downgrades -a myurl="http://finviz.com/screener.ashx?v=110&s=n_downgrades" &
