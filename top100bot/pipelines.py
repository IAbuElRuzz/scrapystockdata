from scrapy.exceptions import DropItem
import json
from scrapy.utils.project import get_project_settings
import MySQLdb
import MySQLdb.cursors
from .items import Stock, FdaStock
settings = get_project_settings()

class UpdatedbPipeline(object):
    insert_stock_sql = """insert into stockdata_stock (%s) values ( %s )"""
    insert_fdastock_sql = """insert into stockdata_fdastock (%s) values ( %s )"""

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
        #print item
        if isinstance(item, Stock):
            self.insert_data(item, self.insert_stock_sql)
            return item
        elif isinstance(item, FdaStock):
            self.insert_data(item, self.insert_fdastock_sql)
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
