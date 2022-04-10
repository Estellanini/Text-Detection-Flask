# flask配置
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_HOST = 127.0.0.1
FLASK_RUN_PORT = 5000

# pear admin flask配置
SYSTEM_NAME = 图片敏感文本检测系统

# MySql配置信息
MYSQL_HOST=127.0.0.1
# MYSQL_HOST=dbserver
MYSQL_PORT=3306
MYSQL_DATABASE=BisheFlask
MYSQL_USERNAME=root
MYSQL_PASSWORD=1234

# Redis 配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# 密钥配置(记得改)
SECRET_KEY='pear-admin-flask'

# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USERNAME='123@qq.com'
MAIL_PASSWORD='XXXXX' # 生成的授权码