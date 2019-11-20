"""
    MinIO [https://docs.min.io/cn/python-client-quickstart-guide.html]
    S3 client

"""

from minio import Minio
from minio.error import ResponseError

import config


class MinioApi:

    def __init__(self):
        self.client = None
        self.initial()

    def initial(self):
        if all([
            config.MINIO_SECRET_ID,
            config.MINIO_SECRET_KEY,
            config.MINIO_SOURCE_URI
        ]):
            self.client = Minio(
                endpoint=config.MINIO_SOURCE_URI,
                access_key=config.MINIO_SECRET_ID,
                secret_key=config.MINIO_SECRET_KEY,
                secure=True
            )

    def upload(self, origin_path, key):
        if self.client is not None:
            try:
                resp = self.client.fput_object(
                    bucket_name=config.MINIO_BUCKET,
                    object_name=key,
                    file_path=origin_path
                )
                return True, resp
            except ResponseError as e:
                print("Exception in MinIO upload. errors: {}".format(e))
                return False, {'msg': e.message}


minio_api = MinioApi()
