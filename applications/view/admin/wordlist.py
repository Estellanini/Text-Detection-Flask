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
from applications.models import Wordlist
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

#
# # 敏感词分类增加
# @admin_wordkinds.get('/add')
# @authorize("admin:wordkinds:add", log=True)
# def add():
#     return render_template('admin/wordkinds/add.html')
#
#
# @admin_wordkinds.post('/save')
# @authorize("admin:wordkinds:add", log=True)
# def save():
#     req_json = request.json
#     kindname = xss_escape(req_json.get('kindname'))
#     remark = xss_escape(req_json.get('remark'))
#     enable = xss_escape(req_json.get("enable"))
#     sort = xss_escape(req_json.get("sort"))
#
#
#     if not kindname:
#         return fail_api(msg="分类名称不得为空")
#
#     if bool(Wordkinds.query.filter_by(kindname=kindname).count()):
#         return fail_api(msg="该分类已经存在")
#     wordkinds = Wordkinds(
#         kindname=kindname,
#         enable=enable,
#         remark=remark,
#         sort=sort
#     )
#     db.session.add(wordkinds)
#     db.session.commit()
#     return success_api(msg="新增成功")
#
#
# # 删除用户
# @admin_wordkinds.delete('/remove/<int:id>')
# @authorize("admin:wordkinds:remove", log=True)
# def delete(id):
#     wordkinds = Wordkinds.query.filter_by(id=id).first()
#     Wordkinds.role = []
#
#     res = Wordkinds.query.filter_by(id=id).delete()
#     db.session.commit()
#     if not res:
#         return fail_api(msg="删除失败")
#     return success_api(msg="删除成功")
#
#
#
#
# #  敏感词分类编辑
# @admin_wordkinds.get('/edit/<int:id>')
# @authorize("admin:wordkinds:edit", log=True)
# def edit(id):
#     wordkinds_id = get_one_by_id(model=Wordkinds, id=id)
#     return render_template('admin/wordkinds/edit.html', wordkinds=wordkinds_id)
#
#
# #  更新分类
# @admin_wordkinds.put('/update')
# @authorize("admin:wordkinds:edit", log=True)
# def update():
#     req_json = request.json
#     id = req_json.get("id")
#     data = {
#         "kindname": xss_escape(req_json.get("kindname")),
#         "sort": xss_escape(req_json.get("sort")),
#         "enable": xss_escape(req_json.get("enable")),
#         "remark": xss_escape(req_json.get("remark"))
#     }
#     wordkinds = Wordkinds.query.filter_by(id=id).update(data)
#     db.session.commit()
#     if not wordkinds:
#         return fail_api(msg="更新敏感词分类失败")
#     return success_api(msg="更新敏感词分类成功")
#
# # 启用该分类
# @admin_wordkinds.put('/enable')
# @authorize("admin:wordkinds:edit", log=True)
# def enable():
#     _id = request.json.get('Id')
#     if _id:
#         res = enable_status(model=Wordkinds, id=_id)
#         if not res:
#             return fail_api(msg="出错啦")
#         return success_api(msg="启用成功")
#     return fail_api(msg="启用失败")
#
#
# # 禁用该分类
# @admin_wordkinds.put('/disable')
# @authorize("admin:wordkinds:edit", log=True)
# def dis_enable():
#     _id = request.json.get('Id')
#     if _id:
#         res = disable_status(model=Wordkinds, id=_id)
#         if not res:
#             return fail_api(msg="出错啦")
#         return success_api(msg="禁用成功")
#     return fail_api(msg="禁用失败")
#
#
# # 批量删除
# @admin_wordkinds.delete('/batchRemove')
# @authorize("admin:wordkinds:remove", log=True)
# def batch_remove():
#     ids = request.form.getlist('ids[]')
#     for id in ids:
#         wordkinds = Wordkinds.query.filter_by(id=id).first()
#         res = Wordkinds.query.filter_by(id=id).delete()
#         db.session.commit()
#     return success_api(msg="批量删除成功")