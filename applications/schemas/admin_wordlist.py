from applications.extensions import ma
from marshmallow import fields


# 敏感词分类的models的序列化类
class WordlistSchema(ma.Schema):
    id = fields.Integer()
    wordname = fields.Str()
    enable = fields.Integer()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
