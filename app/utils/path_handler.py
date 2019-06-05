import hashlib
import time
from pathlib import Path

import config


async def generate_hash_name(filename):
    """
    基于原始文件名生成存储的文件名(含有文件夹)
    :param filename:
    :return:
    """
    p = Path(filename)
    salt_name = str(int(time.time())) + '-' + p.stem
    hash_stem = hashlib.md5(salt_name.encode('utf-8')).hexdigest()
    hash_name = hash_stem + p.suffix
    path_prefix = '/'.join([hash_stem[0:4], hash_stem[4:8]])
    return hash_name, path_prefix


CONSTANT_CHAR = config.BASE_CHAR
CONSTANT_LENGTH = len(CONSTANT_CHAR)


# TODO
async def generate_hash_id():
    source = int(time.time_ns())
    code_arr = ''
    while source > 0:
        code_arr += CONSTANT_CHAR[source % CONSTANT_LENGTH]
        source //= CONSTANT_LENGTH
    return code_arr[::-1].rjust(10, CONSTANT_CHAR[0])
