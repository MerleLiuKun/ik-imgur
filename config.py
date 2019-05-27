# the module config.

DEBUG = True

# DB setting
DB_URL = 'database url'

# 62 char to generate hash id.
BASE_CHAR = '9HfX34CFYmtWnpJsBVy8jlSNorichga2w1bEPvxLTA6MduKRQIe0qDUk5OGZz7'

# up file
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
MAX_FILE_SIZE = 1024 * 1024 * 10
UPLOAD_FOLDER = 'path/to/upload'

try:
    from local_settings import *  # noqa
except ImportError:
    pass
