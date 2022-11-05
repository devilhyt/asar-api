from flask import Flask
import datetime
from pathlib import Path
import os
import secrets

ASAR_ROOT = '.'
ASAR_DATA_ROOT = '/data'
ASAR_PRJ_DIR_NAME = 'asar_projects'

ASAR_PRJ_DIR = f'{ASAR_DATA_ROOT}/{ASAR_PRJ_DIR_NAME}'
ASAR_TEMPLATES_DIR = f'{ASAR_ROOT}/asar_api/assets/templates'
RASA_ACTIONS_ROOT = os.getenv('RASA_ACTIONS_ROOT', '/actions')

OUTPUT_DIR_NAME = 'output'

INTENTS_FILE_NAME = 'intents.json'
RESPONSES_FILE_NAME = 'responses.json'
ACTIONS_FILE_NAME = 'actions.json'
ENTITIES_FILE_NAME = 'entities.json'
SLOTS_FILE_NAME = 'slots.json'
STORIES_FILE_NAME = 'stories.json'
RULES_FILE_NAME = 'rules.json'
TRAINING_DATA_FILE_NAME = 'training_data.yml'
ACTIONS_PY_NAME = 'actions.py'
GCONFIG_FILE_NAME = 'gconfig.json'
LCONFIG_FILE_NAME = 'lconfig.yml'
ACTIONS_J2_NAME = 'action.j2'
SYNONYMS_FILE_NAME ='synonyms.json'
FORMS_FILE_NAME = 'forms.json'

class DevelopmentConfig(object):
    """Flask Config"""

    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex())
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(ASAR_DATA_ROOT).resolve()}/asar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    
    @classmethod
    def init_app(cls, app:Flask):
        app.json.sort_keys = False
        app.json.ensure_ascii = False
