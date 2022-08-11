from flask import Flask
import datetime

WINGMAN_ROOT = 'C:/Users/DevilHYT/Desktop/github/wingman-api'
WINGMAN_DATA_DIR_NAME = 'wingman_data'
WINGMAN_PRJ_DIR_NAME = 'wingman_projects'

WINGMAN_DATA_DIR = f'{WINGMAN_ROOT}/{WINGMAN_DATA_DIR_NAME}'
WINGMAN_PRJ_DIR = f'{WINGMAN_DATA_DIR}/{WINGMAN_PRJ_DIR_NAME}'

INTENTS_DIR_NAME = 'intents'
ACTIONS_DIR_NAME = 'actions'
ENTITIES_DIR_NAME = 'entities'
STORIES_DIR_NAME = 'stories'
RULES_DIR_NAME = 'rules'
TOKENS_DIR_NAME = 'tokens'
MODELS_DIR_NAME = 'models'

INTENTS_FILE_NAME = 'intents.json'
ACTIONS_FILE_NAME = 'actions.json'
ENTITIES_FILE_NAME = 'entities.json'
STORIES_FILE_NAME = 'stories.json'
RULES_FILE_NAME = 'rules.json'
TOKENS_FILE_NAME = 'tokens.json'
JIEBA_DICT_NAME = 'userdict.txt'

class DevelopmentConfig(object):
    """Flask Config"""

    SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{WINGMAN_ROOT}/{WINGMAN_DATA_DIR_NAME}/user.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    JWT_TOKEN_LOCATION = ['headers', 'cookies', 'query_string', 'json']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    
def init_app(app:Flask):
    app.json.sort_keys = False
