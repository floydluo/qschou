import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, Integer, Table, UnicodeText
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

def sdb_connect(basedir, name = "data"):
    return create_engine("sqlite:///" + os.path.join(basedir, name + ".sqlite"))

def mdb_connect():
    MySQL_DB = 'mysql+mysqlconnector://root:freud211@@localhost:3306/qschou?charset=utf8'
    return create_engine(MySQL_DB)



Base = declarative_base()

def create_table(engine):
    Base.metadata.create_all(engine)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key = True)
    timestamp = Column('timestamp', Integer)
    entity = Column('entity',String(100))
    transaction_id = Column('transaction_id', Integer)
    amount = Column('amount', Integer)

    user_uuid = Column('user_uuid',UnicodeText)

    '''
    user = relationship("User", back_populates = "transactions")
    comments = relationship("Comment", back_populates = "transaction")
    '''

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    nickname = Column("nickname", UnicodeText)
    url = Column("url", UnicodeText)
    uuid = Column("uuid", UnicodeText)
    avatar = Column('avatar', UnicodeText)

    '''
    transactions = relationship("Transaction", back_populates = "user")
    send_comments = relationship("Comment", back_populates = "receiver")
    receive_comments = relationship("Comment", back_populates = "sender")
    '''

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key = True)
    content = Column("content", UnicodeText)
    refer = Column("refer", String(60))
    comment_id = Column("comment_id", Integer)

    receiver_uuid = Column('receiver_uuid',UnicodeText)
    #receiver_uuid = Column(Integer, ForeignKey('users.uuid'))
    #receiver = relationship("User", back_populates = "receive_comments")

    sender_uuid = Column("sender_uuid", UnicodeText)
    #sender = relationship("User", back_populates = "send_comments")

    transaction_id = Column("transaction_id",Integer)
    #transaction = relationship("Transaction", back_populates = "comments")
