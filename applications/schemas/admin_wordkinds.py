from applications.extensions import ma
from marshmallow import fields


# 敏感词分类的models的序列化类
class WordkindsSchema(ma.Schema):
    id = fields.Integer()
    kindname = fields.Str()
    enable = fields.Integer()
    remark = fields.Str()
    sort = fields.Integer()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
