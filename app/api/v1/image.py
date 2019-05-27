from pathlib import Path

from PIL import Image as PILImage
from sanic import Blueprint
from sanic.response import json

import config
from app.models import Image
from app.utils.path_handler import generate_hash_name, generate_hash_id

bp = Blueprint('image')


def allowed_file(filename):
    p = Path(filename)
    return p.suffix in config.ALLOWED_EXTENSIONS


@bp.route('/image/simple/upload', methods=['POST'])
async def uploader(request):
    image_file = request.files.get('file')

    # check file extensions
    if not allowed_file(image_file.name):
        return json({
            'status_code': 10001,
            'msg': 'file not allowed.'
        })

    # do save
    name, path_prefix = await generate_hash_name(image_file.name)

    saved_dir = Path(config.UPLOAD_FOLDER + path_prefix)
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

        obj = await Image.create(
            name=name,
            filename=image_file.name,
            size=saved_file.stat().st_size,
            width=width,
            height=height,
            path=relative_path
        )
        return json({
            'status_code': 200,
            'msg': 'ok',
            'data': {
                'image_id': obj.hash_id,
                'url': config.VISIT_URI_PREFIX + obj.path,
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
