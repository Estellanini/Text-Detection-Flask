import os
from flask import Blueprint, request, render_template, jsonify, current_app

from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.rights import authorize
from applications.extensions import db
from applications.models import Photo
from applications.common.utils import upload as upload_curd

admin_ocr = Blueprint('adminOcr', __name__, url_prefix='/admin/ocr')


#  图片检测页面
@admin_ocr.get('/')
@authorize("admin:ocr:main", log=True)
def index():
    return render_template('admin/ocr/main.html')

# 图片上传
@admin_ocr.get('/upload')
def upload():
    return render_template('admin/ocr/main.html')


#   上传接口
@admin_ocr.post('/upload')
def upload_api():
    if 'file' in request.files:
        photo = request.files['file']
        mime = request.files['file'].content_type

        file_url = upload_curd.upload_one(photo=photo, mime=mime)
        res = {
            "msg": "上传成功",
            "code": 0,
            "success": True,
            "data":
                {"src": file_url}
        }
        return jsonify(res)
    return fail_api()
