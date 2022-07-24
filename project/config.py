import datetime

WINGMAN_ROOT = 'C:/Users/DevilHYT/Desktop/github/wingman-api'
WINGMAN_DATA_DIR_NAME = 'wingman-data'
WINGMAN_PRJ_DIR_NAME = 'wingman-projects'

INTENTS_FILE_NAME = 'intents.json'
ACTIONS_FILE_NAME = 'actions.json'

WINGMAN_PRJ_STRUCT = {'intents': [INTENTS_FILE_NAME], 'actions': [ACTIONS_FILE_NAME], 'storys': [], 'rules': [], 'models': []}

WINGMAN_DATA_DIR = f'{WINGMAN_ROOT}/{WINGMAN_DATA_DIR_NAME}'
WINGMAN_PRJ_DIR = f'{WINGMAN_DATA_DIR}/{WINGMAN_PRJ_DIR_NAME}'


class DevelopmentConfig(object):
    """Flask Config"""

    SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    JWT_TOKEN_LOCATION = ['headers', 'cookies', 'query_string', 'json']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
