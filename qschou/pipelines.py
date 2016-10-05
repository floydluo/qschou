# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from sqlalchemy.orm import sessionmaker
from qschou.models import Transaction, User, Comment, sdb_connect,mdb_connect, create_table


class QschouPipeline(object):

    def __init__(self):
        engine = mdb_connect()
        #engine = sdb_connect(os.getcwd())
        create_table(engine)
        Session = sessionmaker(bind = engine)
        self.session = Session()

    def process_item(self, item, spider):
        if 'amount' in item:
            transaction = Transaction(**item)
            try:
                self.session.add(transaction)
            except:
                self.session.rollback()
                raise

        if 'avatar' in item:
            user = self.session.query(User).filter_by(uuid = item['uuid']).first()
            if user == None:
                try:
                    user = User(**item)
                    self.session.add(user)
                except:
                    self.session.rollback()
                    raise
            else:
                pass

        if 'comment_id' in item:
            comment = Comment(**item)
            try:
                self.session.add(comment)
            except:
                self.session.rockback
                raise

        self.session.commit()

        return item
