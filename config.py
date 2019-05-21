# the module config.

DEBUG = True

# DB setting
DB_URL = 'sqlite://data/db.sqlite'

# 62 char to generate hash id.
BASE_CHAR = '9HfX34CFYmtWnpJsBVy8jlSNorichga2w1bEPvxLTA6MduKRQIe0qDUk5OGZz7'

# up file
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 1024 * 1024 * 10
UPLOAD_FOLDER = '/Users/merlin/projects/MyProjects/ik-imgur/var/files/'

try:
    from local_settings import *
except ImportError:
    pass
