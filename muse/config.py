import os

_MUSE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = os.path.join(_MUSE_DIR, '../data/muse.db')
TEMP_FILE_DIR = os.path.join(_MUSE_DIR, '../temp')
API_HOST = 'http://localhost:8080'
