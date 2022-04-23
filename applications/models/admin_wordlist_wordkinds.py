from applications.extensions import db

# 创建中间表
wordlist_wordkinds = db.Table(
    "admin_wordlist_wordkinds",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("wordlist_id", db.Integer, db.ForeignKey("admin_wordlist.id"), comment='敏感词ID'),  # 属性 外键
    db.Column("wordkinds_id", db.Integer, db.ForeignKey("admin_wordkinds.id"), comment='分类ID'),  # 属性 外键
)
