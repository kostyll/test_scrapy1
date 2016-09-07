# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from proxies.items import ProxiesItem
from scrapy.exceptions import DropItem


Base = declarative_base()


class ProxyTable(Base):
    __tablename__ = 'proxiesdata'
    id = Column(Integer, primary_key=True)
    ipAddress = Column('ip_address', String)
    port = Column('port', String)

    def __init__(self, ipAddress, port):
        self.ipAddress=ipAddress
        self.port=port

    def __repr__(self):
        return "<Data %s, %s>" % (self.ipAddress, self.port)


class ProxiesPipeline(object):
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
        self.fio = set()

    def process_item(self, item, spider):
    	if isinstance(item, ProxiesItem):
	    	pt = ProxyTable(item['ipAddress'], item['port'])
	    	self.session.add(pt)
	    	return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)

