# the module config.

DEBUG = True
SENTRY_DSN = ''

# DB setting
DB_URL = 'database url'

# 62 char to generate hash id.
BASE_CHAR = '9HfX34CFYmtWnpJsBVy8jlSNorichga2w1bEPvxLTA6MduKRQIe0qDUk5OGZz7'

# up file
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
MAX_FILE_SIZE = 1024 * 1024 * 10
UPLOAD_FOLDER = 'path/to/upload/'
VISIT_URI = 'your domain'

# 对于上传到云存储的只保存到临时路径，定时清理
TEMP_FILE_FOLDER = 'path/to/temp'

# T cos
COS_SECRET_ID = ''
COS_SECRET_KEY = ''
COS_REGION = ''
COS_BUCKET = ''
COS_VISIT_URI = ''

try:
    from local_settings import *  # noqa
except ImportError:
    pass
