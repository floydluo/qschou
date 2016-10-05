import json
import math

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from scrapy import Spider
from scrapy.http import Request

from qschou.items import TransactionItem, UserItem, CommentItem

def para(id):
    return "?pageIndex=1&timestamp=1475597089_%d&id=%d"%(id, id)

class QSChouSpider(Spider):
    name = "qschou"
    baseurl = "http://support.qschou.com/new/support/a72ee063-48e2-49d9-b356-88d53ce4a076"
    start_urls = [baseurl]

    def parse(self, response):
        body_dic = json.loads(response.body.decode('utf-8'))
        trans = body_dic['data']
        if len(trans) != 0:
            for tran in trans:
                l_tran = ItemLoader(item = TransactionItem(), response = response)
                l_tran.default_output_processor = TakeFirst()
                # here the "response = response" may not necessary, anyway.

                l_tran.add_value("timestamp", tran["created"])
                l_tran.add_value("entity", tran['entity'])
                l_tran.add_value("amount", float(tran['title'][1]['text']))
                l_tran.add_value("transaction_id", tran['id'])
                l_tran.add_value("user_uuid", tran['user']['uuid'])
                yield l_tran.load_item()

                user = tran['user']
                l_user = ItemLoader(item = UserItem())
                l_user.default_output_processor = TakeFirst()
                l_user.add_value("avatar", user['avatar'])
                l_user.add_value("nickname", user["nickname"])
                l_user.add_value("url",user["url"])
                l_user.add_value("uuid", user['uuid'])
                yield l_user.load_item()

                for comment in tran["comments"]:
                    l_com = ItemLoader(item = CommentItem())
                    l_com.default_output_processor = TakeFirst()
                    l_com.add_value("comment_id", comment["comment_id"])
                    l_com.add_value("content", comment['content'])
                    l_com.add_value("refer", comment["refer"])

                    l_com.add_value('transaction_id', tran['id'])
                    l_com.add_value("receiver_uuid", tran['user']['uuid'])
                    l_com.add_value("sender_uuid", comment['sender']['uuid'])

                    yield l_com.load_item()

                    sender = comment['sender']
                    l_sender = ItemLoader(item = UserItem())
                    l_sender.default_output_processor = TakeFirst()
                    l_sender.add_value('avatar', sender['avatar'])
                    l_sender.add_value('nickname', sender['nickname'])
                    l_sender.add_value('url', sender['url'])
                    l_sender.add_value('uuid', sender['uuid'])
                    l_sender.load_item()

            last = trans[-1]
            para_id = last['id']
            yield Request(self.baseurl+para(para_id), callback = self.parse)
