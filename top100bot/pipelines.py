from scrapy.exceptions import DropItem
import json
from scrapy.utils.project import get_project_settings
import MySQLdb
import MySQLdb.cursors

settings = get_project_settings()

class UpdatedbPipeline(object):
    insert_sql_topgainer = """insert into topgainer (%s) values ( %s )"""
    insert_sql_toploser = """insert into toploser (%s) values ( %s )"""
    insert_sql_newhigh = """insert into newhigh (%s) values ( %s )"""
    insert_sql_newlow = """insert into newlow (%s) values ( %s )"""
    insert_sql_unusualvolume = """insert into unusualvolume (%s) values ( %s )"""
    insert_sql_overbought = """insert into overbought (%s) values ( %s )"""
    insert_sql_oversold = """insert into oversold (%s) values ( %s )"""
    insert_sql_mostvolatile = """insert into mostvolatile (%s) values ( %s )"""
    insert_sql_mostactive = """insert into mostactive (%s) values ( %s )"""
    insert_sql_upgrades = """insert into upgrades (%s) values ( %s )"""
    insert_sql_downgrades = """insert into downgrades (%s) values ( %s )"""

    def __init__(self):
        db = MySQLdb.connect(
            host=settings.get('DB_CONNECT')['host'],    # your host, usually localhost
            user=settings.get('DB_CONNECT')['user'],         # your username
            passwd=settings.get('DB_CONNECT')['passwd'],  # your password
            db=settings.get('DB_CONNECT')['db']
        )        # name of the data base
        self.dbpool = db
        print settings.get('DB_CONNECT')['host']
        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        self.cur = db.cursor()

    def __del__(self):
	    self.dbpool.close()

    def process_item(self, item, spider):

        if spider.name == "topgainerbot":
            self.insert_data(item, self.insert_sql_topgainer)
        elif spider.name == "toploserbot":
            self.insert_data(item, self.insert_sql_toploser)
        elif spider.name == "newhighbot":
            self.insert_data(item, self.insert_sql_newhigh)
        elif spider.name == "newlowbot":
            self.insert_data(item, self.insert_sql_newlow)
        elif spider.name == "unusualvolumebot":
            self.insert_data(item, self.insert_sql_unusualvolume)
        elif spider.name == "overboughtbot":
            self.insert_data(item, self.insert_sql_overbought)
        elif spider.name == "oversoldbot":
            self.insert_data(item, self.insert_sql_oversold)
        elif spider.name == "mostvolatilebot":
            self.insert_data(item, self.insert_sql_mostvolatile)
        elif spider.name == "mostactivebot":
            self.insert_data(item, self.insert_sql_mostactive)
        elif spider.name == "upgradesbot":
            self.insert_data(item, self.insert_sql_upgrades)
        elif spider.name == "downgradesbot":
            self.insert_data(item, self.insert_sql_downgrades)

        return item

    def insert_data(self, item, insert):
        tmp_keys = item.fields.keys()
        values = []
        keys = []
        for k in tmp_keys:
            keys.append("`"+str(k)+"`")
            values.append("'"+str(item[k])+"'")
        fields = u','.join(keys)
        qm = u','.join(values)
        sql = insert % (fields, qm)
        #print sql
        return self.cur.execute(sql)

