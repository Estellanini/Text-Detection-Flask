import datetime
from applications.extensions import db


class Wordlist(db.Model):
    __tablename__ = 'admin_wordlist'
    id = db.Column(db.Integer, primary_key=True, comment='敏感词ID')
    wordname = db.Column(db.String(255), comment='敏感词名称')
    word_kindid = db.relationship('Wordkinds',secondary="admin_wordlist_wordkinds",backref=db.backref('wordlist'), lazy='dynamic')
    enable = db.Column(db.Integer, comment='是否启用')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')
