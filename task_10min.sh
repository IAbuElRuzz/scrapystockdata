#! /bin/sh    
export PATH=$PATH:/usr/local/bin
cd /Users/ethanzhang/PycharmProjects/top100bot

scrapy crawl topgainersbot -a category=topgainers -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_topgainers" &
scrapy crawl topgainersbot -a category=toplosers -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_toplosers" &
scrapy crawl topgainersbot -a category=unusualvolumes -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_unusualvolume" &
