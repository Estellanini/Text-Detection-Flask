from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import model_to_dicts, enable_status, disable_status,get_one_by_id
from applications.common.helper import ModelFilter
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import xss_escape
from applications.extensions import db
from applications.models import Wordlist, Wordkinds
from applications.schemas import WordlistSchema

admin_wordlist = Blueprint('adminWordlist', __name__, url_prefix='/admin/wordlist')


# 敏感词列表管理
@admin_wordlist.get('/')
@authorize("admin:wordlist:main", log=True)
def main():
    return render_template('admin/wordlist/main.html')


#   敏感词分类分页查询
@admin_wordlist.get('/data')
@authorize("admin:wordlist:main", log=True)
def data():
    # 获取请求参数
    wordname = xss_escape(request.args.get('wordname', type=str))
    # 查询参数构造
    mf = ModelFilter()
    if wordname:
        mf.contains(field_name="wordname", value=wordname)
    # orm查询
    # 使用分页获取data需要.items
    wordlist = Wordlist.query.filter(mf.get_filter(model=Wordlist)).layui_paginate()
    count = wordlist.total
    # 返回api
    return table_api(data=model_to_dicts(schema=WordlistSchema, data=wordlist.items), count=count)


# 敏感词增加
@admin_wordlist.get('/add')
@authorize("admin:wordlist:add", log=True)
def add():
    wordkinds = Wordkinds.query.all()
    return render_template('admin/wordlist/add.html',wordkinds=wordkinds)


@admin_wordlist.post('/save')
@authorize("admin:wordlist:add", log=True)
def save():
    req_json = request.json
    a = req_json.get("kindIds")
    wordname = xss_escape(req_json.get('wordname'))
    enable = xss_escape(req_json.get("enable"))
    kind_ids = a.split(',')

    if not wordname:
        return fail_api(msg="敏感词名称不得为空")

    if bool(Wordlist.query.filter_by(wordname=wordname).count()):
        return fail_api(msg="敏感词已经存在")
    wordlist = Wordlist(
        wordname=wordname,
        enable=enable,
        # word_kindid=a
    )
    db.session.add(wordlist)
    wordkinds = Wordkinds.query.filter(Wordkinds.id.in_(kind_ids)).all()
    for r in wordkinds:
        wordlist.word_kindid.append(r)
    db.session.commit()
    return success_api(msg="新增成功")


# 删除敏感词
@admin_wordlist.delete('/remove/<int:id>')
@authorize("admin:wordlist:remove", log=True)
def delete(id):
    wordlist = Wordlist.query.filter_by(id=id).first()
    wordlist.word_kindid = []

    res = Wordlist.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")




#  敏感词编辑
@admin_wordlist.get('/edit/<int:id>')
@authorize("admin:wordlist:edit", log=True)
def edit(id):
    wordlist = get_one_by_id(model=Wordlist, id=id)
    wordkinds = Wordkinds.query.all()
    checked_wordkinds = []
    for w in wordlist.word_kindid:
        checked_wordkinds.append(w.id)
    return render_template('admin/wordlist/edit.html', wordlist=wordlist,wordkinds=wordkinds,checked_wordkinds=checked_wordkinds)


#  更新敏感词
@admin_wordlist.put('/update')
@authorize("admin:wordlist:edit", log=True)
def update():
    req_json = request.json
    id = req_json.get("id")
    data = {
        "wordname": xss_escape(req_json.get("wordname")),
        "enable": xss_escape(req_json.get("enable")),
        # "word_kindid": xss_escape(req_json.get("kind_ids"))
    }
    wordlist = Wordlist.query.filter_by(id=id).update(data)
    db.session.commit()
    if not wordlist:
        return fail_api(msg="更新敏感词失败")
    return success_api(msg="更新敏感词成功")

# 启用该词
@admin_wordlist.put('/enable')
@authorize("admin:wordlist:edit", log=True)
def enable():
    _id = request.json.get('Id')
    if _id:
        res = enable_status(model=Wordlist, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启用成功")
    return fail_api(msg="启用失败")


# 禁用该词
@admin_wordlist.put('/disable')
@authorize("admin:wordlist:edit", log=True)
def dis_enable():
    _id = request.json.get('Id')
    if _id:
        res = disable_status(model=Wordlist, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="禁用失败")


# 批量删除
@admin_wordlist.delete('/batchRemove')
@authorize("admin:wordlist:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        wordlist = Wordkinds.query.filter_by(id=id).first()
        res = Wordkinds.query.filter_by(id=id).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")