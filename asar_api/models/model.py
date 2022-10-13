import os
from pathlib import Path
from typing import Tuple
from datetime import datetime
import requests
from ..config import OUTPUT_DIR_NAME, TRAINING_DATA_FILE_NAME
from ..models.server_status import ServerStatus
from ..extensions import db


class Model:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(OUTPUT_DIR_NAME)
        self.model_file = self.dir.joinpath(f'{prj_name}.tar.gz')
        self.training_data_file = self.dir.joinpath(TRAINING_DATA_FILE_NAME)
        # env var
        self.env_rasa_api_url = os.getenv("RASA_API_URL")
        self.env_asar_api_url = os.getenv("ASAR_API_URL")

    def init(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)

    def check_health(self, rasa_api_url) -> bool:
        try:
            resp = requests.get(url=f'{rasa_api_url}')
            return resp.status_code == requests.codes.ok
        except:
            return False

    def train(self, debug=False, custom_rasa_api_url=None, custom_asar_api_url=None) -> Tuple[int, str]:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        asar_api_url = custom_asar_api_url or self.env_asar_api_url
        server_status = ServerStatus.query.first()

        if debug:
            server_status.training_result = 1
            server_status.training_message = 'debug mode'
            server_status.training_project = self.prj_name
            server_status.training_time = datetime.now()
            db.session.commit()
            return 200, 'debug mode'
        elif server_status.loaded_status:
            return 400, f'Still performing previous loading task.'
        elif server_status.training_status:
            return 400, f'Still performing previous training. (Project: {server_status.training_project})'
        elif not (rasa_api_url and asar_api_url):
            return 400, 'Please provide RASA_API_URL and ASAR_API_URL.'
        else:
            params = {'save_to_default_model_directory': 'false',
                      'force_training': 'true',
                      'callback_url': f'{asar_api_url}/projects/{self.prj_name}/models'}

            if self.check_health(rasa_api_url):
                if self.prj_name == server_status.loaded_project:
                    # unload model
                    _ = requests.delete(url=f'{rasa_api_url}/model')
                    server_status.loaded_project = None
                    db.session.commit()

                with open(self.training_data_file, 'r', encoding="utf-8") as f:
                    data = f.read()
                _ = requests.post(url=f'{rasa_api_url}/model/train',
                                  params=params,
                                  data=data.encode('utf-8'))

                server_status.training_status = True
                server_status.training_result = -1
                server_status.training_project = self.prj_name
                server_status.training_time = datetime.now()
                server_status.training_message = None
                db.session.commit()
                return 200, 'OK'
            else:
                return 400, 'Can not connect to Rasa API server.'
            

    def load_checker(self, debug=False, custom_rasa_api_url=None) -> Tuple[int, str]:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        server_status = ServerStatus.query.first()

        if debug:
            return 200, 'debug mode'
        elif not rasa_api_url:
            return 400, 'Please provide RASA_API_URL.'
        elif server_status.loaded_status:
            return 400, f'Still performing previous loading task.'
        elif server_status.training_project == self.prj_name and server_status.training_status:
            return 400, f'Can not load a project which is training.'
        else:
            if self.check_health(rasa_api_url):
                return 200, 'OK'
            else:
                return 400, 'Can not connect to Rasa API server.'

    def load_bg(self, debug=False, custom_rasa_api_url=None) -> bool:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        server_status = ServerStatus.query.first()

        if debug:
            server_status.loaded_result = 1
            server_status.loaded_message = 'debug mode'
            server_status.loaded_project = self.prj_name
            server_status.loaded_time = datetime.now()
            db.session.commit()
            return True
        else:
            data = {'model_file': self.model_file.absolute().as_posix()}

            server_status.loaded_status = True
            server_status.loaded_result = -1
            server_status.loaded_message = None
            server_status.loaded_project = None
            server_status.loaded_time = datetime.now()
            db.session.commit()

            try:
                # long time request
                resq = requests.put(url=f'{rasa_api_url}/model',
                                        json=data,
                                        timeout=300)
                if resq.status_code == 204:
                    server_status.loaded_status = False
                    server_status.loaded_result = 1
                    server_status.loaded_message = 'OK'
                    server_status.loaded_project = self.prj_name
                    db.session.commit()
                    return True
                else:
                    server_status.loaded_status = False
                    server_status.loaded_result = 0
                    server_status.loaded_message = 'Failed'
                    db.session.commit()
                    return False
            except Exception as e:
                server_status.loaded_status = False
                server_status.loaded_result = 0
                server_status.loaded_message = str(e)
                db.session.commit()
                return False

    def save(self, content) -> None:
        with open(self.model_file, 'wb') as t:
            t.write(content)
