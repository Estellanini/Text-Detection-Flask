import os
from flask import Blueprint, request, render_template, jsonify, current_app

from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.rights import authorize
from applications.extensions import db
from applications.models import Photo
from applications.common.utils import upload as upload_curd

admin_text = Blueprint('adminText', __name__, url_prefix='/admin/text')


#  输入文本管理
@admin_text.get('/')
@authorize("admin:text:main", log=True)
def index():
    return render_template('admin/text/main.html')