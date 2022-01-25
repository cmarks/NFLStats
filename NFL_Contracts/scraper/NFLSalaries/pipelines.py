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

class Contract(base):  
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    player = Column(String, unique=True)
    team = Column(String)
    position = Column(String)
    age = Column(String)
    total_value = Column(Integer)
    avg_year = Column(Integer)
    total_guaranteed = Column(Integer)
    fully_guaranteed = Column(Integer)
    free_agency_year = Column(String)
    free_agency_type = Column(String)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

class DuplicatesPipeline(object):
    def __init__(self):
        self.players = set()

    def process_item(self, item, spider):
        if item["player"] in self.players:
            raise DropItem("This player has already been stored: %s" % item)
        else:
            self.players.add(item["player"])
            return item


class DatabasePipeline(object):
    def __init__(self, db, user, passwd, host):
        return 
        # self.conn = psycopg2.connect(host=host,
        #                             user=user,
        #                             password=passwd,
        #                             database=db)#,
        #                             # unix_socket="/opt/lampp/var/mysql/mysql.sock",
        #                             # charset='utf8', use_unicode=True)
        # self.cursor = self.conn.cursor()
        # self.conn = db.connect() 

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
        # query = ("INSERT INTO Contract (player, team, position, age, total_value, avg_year, "
        #          "total_guaranteed, fully_guaranteed, free_agency_year, free_agency_type)"
        #          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        # self.cursor.execute(query, (item["player"],
        #                             item["team"],
        #                             item["position"],
        #                             item["age"],
        #                             item["total_value"],
        #                             item["avg_year"],
        #                             item["total_guaranteed"],
        #                             item["fully_guaranteed"],
        #                             item["free_agency_year"],
        #                             item["free_agency_type"]
        #                             )
        #                     )
        # self.conn.commit()
        obj = Contract(player=item["player"], team=item["team"], position=item["position"], age=item["age"], total_value=item["total_value"],
                       avg_year=item["avg_year"], total_guaranteed=item["total_guaranteed"], fully_guaranteed=item["fully_guaranteed"], 
                       free_agency_year=item["free_agency_year"], free_agency_type=item["free_agency_type"])  
        session.add(obj)  
        session.commit()  
        return item

    def close_spider(self):
        self.conn.close()