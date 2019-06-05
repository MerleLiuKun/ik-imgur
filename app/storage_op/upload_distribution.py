"""
    提供函数给外部API,
"""
from .cos_api import cos_client


async def upload_file(s_type, origin_path, key):
    """
    依据不同的 存储类型 保存文件
    :param s_type: 类型 (COS)
    :param origin_path: 原始文件路径
    :param key: 存储 Key
    :return:
    """
    # 等于 '' 时 不需要上传
    if s_type == '':
        return True, {}
    elif s_type == 'COS':
        resp = cos_client.upload(
            origin_path=origin_path,
            key=key
        )
    else:
        resp = False, {'msg': 'type not support.'}
    return resp
