#! /bin/sh    
export PATH=$PATH:/usr/local/bin
cd /Users/ethanzhang/PycharmProjects/top100bot

scrapy crawl topgainersbot -a category=newhighs -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_newhigh" &
scrapy crawl topgainersbot -a category=newlows -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_newlow" &
scrapy crawl topgainersbot -a category=overboughts -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_overbought" &
scrapy crawl topgainersbot -a category=oversolds -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_oversold" &
scrapy crawl topgainersbot -a category=mostactives -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_mostactive" &
scrapy crawl topgainersbot -a category=mostvolatiles -a myurl="http://finviz.com/screener.ashx?v=110&s=ta_mostvolatile" &
