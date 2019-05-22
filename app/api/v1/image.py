from pathlib import Path

from PIL import Image as PILImage
from sanic import Blueprint
from sanic.response import json

import config
from app.models import Image
from app.utils.path_handler import generate_hash_name

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
    name, path_prefix = generate_hash_name(image_file.name)

    saved_dir = Path(config.UPLOAD_FOLDER + path_prefix)
    saved_file = saved_dir / name
    if not saved_dir.exists():
        saved_dir.mkdir(parents=True)

    with open(saved_file, 'wb') as f:
        f.write(image_file.body)
    if not saved_file.exists():
        with PILImage.open(saved_file) as img:
            width, height = img.size

        await Image.create(
            name=name,
            filename=image_file.name,
            size=saved_file.stat().st_size,
            width=width,
            height=height,
            path=path_prefix + name
        )
        return json({
            'status_code': 200,
            'msg': 'ok',
        })
    else:
        return json({
            'status_code': 10002,
            'msg': 'error'
        })
