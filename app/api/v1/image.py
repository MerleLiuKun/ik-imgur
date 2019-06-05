from pathlib import Path

from PIL import Image as PILImage
from sanic import Blueprint
from sanic.response import json
from werkzeug.utils import secure_filename

import config
from app.models import Image
from app.storage_op.upload_distribution import upload_file
from app.utils.path_handler import generate_hash_name

bp = Blueprint('image')


def allowed_file(filename):
    p = Path(filename)
    return p.suffix in config.ALLOWED_EXTENSIONS


def build_visit_uri(s_type):
    """
    :param s_type: 存储类型
    :return:
    """
    if s_type == '':
        return config.VISIT_URI
    elif s_type == 'COS':
        return config.COS_VISIT_URI
    else:
        return ''


# TODO 暂时没有发现 sanic 控制上传文件大小的处理
# 暂时以 Nginx 来控制
@bp.route('/image/upload', methods=['POST'])
async def uploader(request):
    image_file = request.files.get('file')

    save_type = request.form.get('save_type')

    if not save_type:
        local_path = config.UPLOAD_FOLDER
    else:
        local_path = config.TEMP_FILE_FOLDER

    # check file extensions
    if not allowed_file(image_file.name):
        return json({
            'status_code': 10001,
            'msg': 'file not allowed.'
        })

    # do save
    name, path_prefix = await generate_hash_name(secure_filename(image_file.name))

    saved_dir = Path(local_path + path_prefix)
    saved_file = saved_dir / name
    # build relative path
    relative_path = '/'.join([path_prefix, name])
    if not saved_dir.exists():
        saved_dir.mkdir(parents=True)

    with open(saved_file, 'wb') as f:
        f.write(image_file.body)
    if saved_file.exists():
        with PILImage.open(saved_file) as img:
            width, height = img.size

        up_status, up_res = await upload_file(
            s_type=save_type,
            origin_path=saved_file,
            key=relative_path
        )
        if not up_status:
            return json({
                'status_code': 10003,
                'msg': up_res['msg']
            })

        obj = await Image.create(
            name=name,
            filename=image_file.name,
            size=saved_file.stat().st_size,
            width=width,
            height=height,
            path=relative_path,
            save_type=save_type
        )
        return json({
            'status_code': 200,
            'msg': 'ok',
            'data': {
                'image_id': obj.hash_id,
                'url': build_visit_uri(save_type) + obj.path,
                'relative_path': obj.path,
                'width': width,
                'height': height,
            }
        })
    else:
        return json({
            'status_code': 10002,
            'msg': 'save error',
        })
