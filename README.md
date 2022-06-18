# Text-Detection-Flask
A demo for a Flask Project
运行flask项目流程
1.新建仓库，将项目拷贝进去
2.更改.flaskenv配置文件中的Mysql_Password和Mysql_DATABASE名字
3.执行flask init进行初始化
4.执行flask run运行项目



二次开发改写代码：
1.applications->view中新增view->admim->xxxxx.py
2.templates->admin中新建文件夹以及html文件，并在view->__init_.py中导入
3.在models中添加xxxx.py文件详细写数据库设计并在modelszhongde __init__.py文件中暴露这个数据模型
4.执行数据库迁移
flask db migrate
flask db upgrade
这时观察数据库，多了新表
5.改applications->view->admin->wordkinds中的请求部分后端代码
6.新增：application->schemas中的Schema 在Schemas->__init__.py中暴露这个数据模型
7.写新增页面 template->admin->wordkinds->add.html
改applications->view->admin->wordkinds.py

