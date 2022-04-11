import datetime
from applications.extensions import db


class Wordkinds(db.Model):
    __tablename__ = 'admin_wordkinds'
    id = db.Column(db.Integer, primary_key=True, comment='敏感词分类ID')
    kindname = db.Column(db.String(255), comment='分类名称')
    enable = db.Column(db.Integer, comment='是否启用')
    remark = db.Column(db.String(255), comment='备注')
    sort = db.Column(db.Integer, comment='排序')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
