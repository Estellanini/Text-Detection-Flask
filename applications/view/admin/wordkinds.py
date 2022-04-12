from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import model_to_dicts, enable_status, disable_status
from applications.common.helper import ModelFilter
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import xss_escape
from applications.extensions import db
from applications.models import Role
from applications.models import User, AdminLog
from applications.models import Wordkinds
from applications.schemas import WordkindsSchema

admin_wordkinds = Blueprint('adminWordkinds', __name__, url_prefix='/admin/wordkinds')


# 敏感词分类管理
@admin_wordkinds.get('/')
@authorize("admin:wordkinds:main", log=True)
def main():
    return render_template('admin/wordkinds/main.html')


#   敏感词分类分页查询
@admin_wordkinds.get('/data')
@authorize("admin:wordkinds:main", log=True)
def data():
    # 获取请求参数
    kindname = xss_escape(request.args.get('kindname', type=str))
    # 查询参数构造
    mf = ModelFilter()
    if kindname:
        mf.contains(field_name="kindname", value=kindname)
    # orm查询
    # 使用分页获取data需要.items
    wordkinds = Wordkinds.query.filter(mf.get_filter(model=Wordkinds)).layui_paginate()
    count = wordkinds.total
    # 返回api
    return table_api(data=model_to_dicts(schema=WordkindsSchema, data=wordkinds.items), count=count)


# 用户增加
@admin_wordkinds.get('/add')
@authorize("admin:wordkinds:add", log=True)
def add():
    return render_template('admin/wordkinds/add.html')


@admin_wordkinds.post('/save')
@authorize("admin:wordkinds:add", log=True)
def save():
    req_json = request.json
    kindname = xss_escape(req_json.get('kindname'))
    remark = xss_escape(req_json.get('remark'))
    enable = xss_escape(req_json.get("enable"))
    sort = xss_escape(req_json.get("sort"))


    if not kindname:
        return fail_api(msg="分类名称不得为空")

    if bool(Wordkinds.query.filter_by(kindname=kindname).count()):
        return fail_api(msg="该分类已经存在")
    wordkinds = Wordkinds(
        kindname=kindname,
        enable=enable,
        remark=remark,
        sort=sort
    )
    db.session.add(wordkinds)
    db.session.commit()
    return success_api(msg="新增成功")

#
# # 删除用户
# @admin_wordkinds.delete('/remove/<int:id>')
# @authorize("admin:user:remove", log=True)
# def delete(id):
#     user = User.query.filter_by(id=id).first()
#     user.role = []
#
#     res = User.query.filter_by(id=id).delete()
#     db.session.commit()
#     if not res:
#         return fail_api(msg="删除失败")
#     return success_api(msg="删除成功")
#
#
# #  编辑用户
# @admin_wordkinds.get('/edit/<int:id>')
# @authorize("admin:user:edit", log=True)
# def edit(id):
#     user = curd.get_one_by_id(User, id)
#     roles = Role.query.all()
#     checked_roles = []
#     for r in user.role:
#         checked_roles.append(r.id)
#     return render_template('admin/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)
#
#
# #  编辑用户
# @admin_wordkinds.put('/update')
# @authorize("admin:user:edit", log=True)
# def update():
#     req_json = request.json
#     a = xss_escape(req_json.get("roleIds"))
#     id = xss_escape(req_json.get("userId"))
#     username = xss_escape(req_json.get('username'))
#     real_name = xss_escape(req_json.get('realName'))
#     dept_id = xss_escape(req_json.get('deptId'))
#     role_ids = a.split(',')
#     User.query.filter_by(id=id).update({'username': username, 'realname': real_name, 'dept_id': dept_id})
#     u = User.query.filter_by(id=id).first()
#
#     roles = Role.query.filter(Role.id.in_(role_ids)).all()
#     u.role = roles
#
#     db.session.commit()
#     return success_api(msg="更新成功")
#
#
#
#
#
#
#
# # 修改当前用户信息
# @admin_wordkinds.put('/updateInfo')
# @login_required
# def update_info():
#     req_json = request.json
#     r = User.query.filter_by(id=current_user.id).update(
#         {"realname": req_json.get("realName"), "remark": req_json.get("details")})
#     db.session.commit()
#     if not r:
#         return fail_api(msg="出错啦")
#     return success_api(msg="更新成功")
#
#
#
# # 启用用户
# @admin_wordkinds.put('/enable')
# @authorize("admin:user:edit", log=True)
# def enable():
#     _id = request.json.get('userId')
#     if _id:
#         res = enable_status(model=User, id=_id)
#         if not res:
#             return fail_api(msg="出错啦")
#         return success_api(msg="启动成功")
#     return fail_api(msg="数据错误")
#
#
# # 禁用用户
# @admin_wordkinds.put('/disable')
# @authorize("admin:user:edit", log=True)
# def dis_enable():
#     _id = request.json.get('userId')
#     if _id:
#         res = disable_status(model=User, id=_id)
#         if not res:
#             return fail_api(msg="出错啦")
#         return success_api(msg="禁用成功")
#     return fail_api(msg="数据错误")
#
#
# # 批量删除
# @admin_wordkinds.delete('/batchRemove')
# @authorize("admin:user:remove", log=True)
# def batch_remove():
#     ids = request.form.getlist('ids[]')
#     for id in ids:
#         user = User.query.filter_by(id=id).first()
#         user.role = []
#
#         res = User.query.filter_by(id=id).delete()
#         db.session.commit()
#     return success_api(msg="批量删除成功")
