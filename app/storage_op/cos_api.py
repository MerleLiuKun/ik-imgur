"""
    tencent cos.
"""
from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosServiceError

import config


class CosApi:

    def __init__(self):
        self.client = None
        self.initial()

    def initial(self):
        if all([config.COS_SECRET_ID, config.COS_SECRET_KEY, config.COS_REGION]):
            cos_config = CosConfig(
                Region=config.COS_REGION,
                SecretId=config.COS_SECRET_ID,
                SecretKey=config.COS_SECRET_KEY
            )
            self.client = CosS3Client(cos_config)

    def upload(self, origin_path, key):
        try:
            resp = self.client.upload_file(
                Bucket=config.COS_BUCKET,
                LocalFilePath=origin_path,
                Key=key,
            )
            return True, resp
        except CosServiceError as e:
            print("Exception in COS upload. errors: {}".format(e.get_digest_msg()))
            return False, {'msg': e.get_error_msg()}


cos_client = CosApi()
