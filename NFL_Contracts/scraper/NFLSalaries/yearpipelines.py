# -*- coding: utf-8 -*-
import MySQLdb
import pymysql
import psycopg2
from scrapy.exceptions import NotConfigured, DropItem
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Table, Column, String, MetaData, Integer
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://postgres:postgres@localhost:5432/nfl"
db = create_engine(db_string)
base = declarative_base()

class ContractYear(base):  
    __tablename__ = 'contract_years'

    id = Column(Integer, primary_key=True)
    player = Column(String, unique=True) 
    team = Column(String)
    position = Column(String)
    year = Column(String)
    cap_number = Column(Integer)
    cash_spent = Column(Integer)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

class DuplicatesPipeline(object):
    def __init__(self):
        self.players = set()

    def process_item(self, item, spider):
        key = item["player"] + item["year"]
        if key in self.players:
            raise DropItem("This player for this year has already been stored: %s" % item)
        else:
            self.players.add(key)
            return item


class DatabasePipeline(object):
    def __init__(self, db, user, passwd, host):
        return 

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings["db"]
        user = db_settings["user"]
        passwd = db_settings["passwd"]
        host = db_settings["host"]
        return cls(db, user, passwd, host)

    def process_item(self, item, spider):
        obj = ContractYear(player=item["player"], team=item["team"], position=item["position"], year=item["year"],
                           cap_number=item["cap_number"], cash_spent=item["cash_spent"])
        session.add(obj)  
        session.commit()  
        return item

    def close_spider(self):
        self.conn.close()