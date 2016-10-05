from scrapy import Item, Field

class TransactionItem(Item):
    timestamp = Field()
    entity = Field()
    transaction_id = Field()
    amount = Field()
    user_uuid = Field()

class UserItem(Item):
    avatar = Field()
    nickname = Field()
    url = Field()
    uuid = Field()

class CommentItem(Item):
    comment_id = Field()
    content = Field()
    refer = Field()

    receiver_uuid = Field()
    sender_uuid = Field()
    transaction_id = Field()
