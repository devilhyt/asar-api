import os
import time
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
        self.rasa_api_protocol = os.getenv('RASA_API_PROTOCOL')
        self.rasa_api_host = os.getenv('RASA_API_HOST')
        self.rasa_api_port = os.getenv('RASA_API_PORT')
        self.asar_api_protocol = os.getenv('ASAR_API_PROTOCOL')
        self.asar_api_host = os.getenv('ASAR_API_HOST')
        self.asar_api_port = os.getenv('ASAR_API_PORT')
        self.rasa_api_agent_protocol = os.getenv('RASA_API_AGENT_PROTOCOL')
        self.rasa_api_agent_host = os.getenv('RASA_API_AGENT_HOST')
        self.rasa_api_agent_port = os.getenv('RASA_API_AGENT_PORT')
        self.asar_api_agent_protocol = os.getenv('ASAR_API_AGENT_PROTOCOL')
        self.asar_api_agent_host = os.getenv('ASAR_API_AGENT_HOST')
        self.asar_api_agent_port = os.getenv('ASAR_API_AGENT_PORT')

        if self.rasa_api_protocol and self.rasa_api_host and self.rasa_api_port:
            self.env_rasa_api_url = f'{self.rasa_api_protocol}://{self.rasa_api_host}:{self.rasa_api_port}'
        else:
            self.env_rasa_api_url = None

        if self.asar_api_protocol and self.asar_api_host and self.asar_api_port:
            self.env_asar_api_url = f'{self.asar_api_protocol}://{self.asar_api_host}:{self.asar_api_port}'
        else:
            self.env_asar_api_url = None

        if self.rasa_api_agent_protocol and self.rasa_api_agent_host and self.rasa_api_agent_port:
            self.env_rasa_api_agent_url = f'{self.rasa_api_agent_protocol}://{self.rasa_api_agent_host}:{self.rasa_api_agent_port}'
        else:
            self.env_rasa_api_agent_url = None

        if self.asar_api_agent_protocol and self.asar_api_agent_host and self.asar_api_agent_port:
            self.env_asar_api_agent_url = f'{self.asar_api_agent_protocol}://{self.asar_api_agent_host}:{self.asar_api_agent_port}'
        else:
            self.env_asar_api_agent_url = None

    def init(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)

    def check_health(self, rasa_api_url) -> bool:
        try:
            resp = requests.get(url=f'{rasa_api_url}', timeout=5)
            return resp.status_code == requests.codes.ok
        except:
            return False

    def train(self, debug=False) -> Tuple[int, str, str]:
        rasa_api_url = self.env_rasa_api_agent_url or self.env_rasa_api_url
        asar_api_url = self.env_asar_api_agent_url or self.env_asar_api_url
        server_status = ServerStatus.query.first()
        msg_prefix = '[debug mode]' if debug else ''

        if server_status.loaded_status:
            return 400, f'{msg_prefix} Still performing previous loading task.', 'stillLoadingPreviousModel'
        elif server_status.training_status:
            return 400, f'{msg_prefix} Still performing previous training (Project: {server_status.training_project}).', 'stillTrainingPreviousModel'
        elif not (rasa_api_url):
            return 400, f'{msg_prefix} Please provide RASA_API_URL.', 'noRasaApiUrlProvided'
        elif not (asar_api_url):
            return 400, f'{msg_prefix} Please provide ASAR_API_URL.', 'noAsarApiUrlProvided'
        else:
            params = {'save_to_default_model_directory': 'false',
                      'force_training': 'true',
                      'callback_url': f'{asar_api_url}/projects/{self.prj_name}/models'}

            if debug:
                server_status.training_status = True
                server_status.training_result = -1
                server_status.training_project = self.prj_name
                server_status.training_time = datetime.now()
                server_status.training_message = None
                db.session.commit()
                return 200, f'{msg_prefix} OK', 'success'
            else:
                if self.check_health(rasa_api_url):
                    # if self.prj_name == server_status.loaded_project:
                    #     # unload model
                    #     _ = requests.delete(url=f'{rasa_api_url}/model')
                    #     server_status.loaded_project = None
                    #     db.session.commit()

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
                    return 200, 'OK', 'success'
                else:
                    return 400, 'Cannot connect to Rasa API server.', 'rasaApiConnectionError'

    def load_checker(self, debug=False) -> Tuple[int, str]:
        rasa_api_url = self.env_rasa_api_url
        server_status = ServerStatus.query.first()
        msg_prefix = '[debug mode]' if debug else ''

        if not rasa_api_url:
            return 400, f'{msg_prefix} Please provide RASA_API_URL.', 'noRasaUrlProvided'
        elif server_status.loaded_status:
            return 400, f'{msg_prefix} Still performing previous loading task.', 'stillLoadingPreviousModel'
        elif server_status.training_project == self.prj_name and server_status.training_status:
            return 400, f'{msg_prefix} Cannot load a project which is training.', 'projectIsTraining'
        else:
            if debug:
                return 200, f'{msg_prefix} OK', 'success'
            else:
                if self.check_health(rasa_api_url):
                    return 200, 'OK', 'success'
                else:
                    return 400, 'Cannot connect to Rasa API server.', 'rasaApiConnectionError'

    def load_bg(self, debug=False) -> bool:
        rasa_api_url = self.env_rasa_api_url
        server_status = ServerStatus.query.first()

        if debug:
            server_status.loaded_status = True
            server_status.loaded_result = -1
            server_status.loaded_message = None
            server_status.loaded_project = None
            server_status.loaded_time = datetime.now()
            db.session.commit()

            time.sleep(3)
            server_status.loaded_status = False
            server_status.loaded_result = 1
            server_status.loaded_message = 'debug mode'
            server_status.loaded_project = self.prj_name
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
        self.unload_model()
        with open(self.model_file, 'wb') as t:
            t.write(content)

    def unload_model(self) -> None:
        """unload model only if required"""

        rasa_api_url = self.env_rasa_api_url
        server_status = ServerStatus.query.first()
        if self.prj_name == server_status.loaded_project:
            if self.check_health(rasa_api_url):
                # unload model
                _ = requests.delete(url=f'{rasa_api_url}/model')
                server_status.loaded_project = None
                # db.session.commit()
