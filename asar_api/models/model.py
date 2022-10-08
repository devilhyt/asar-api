from pathlib import Path
import requests
from ruamel.yaml import YAML
from ..config import OUTPUT_DIR_NAME, TRAINING_DATA_FILE_NAME
import os
from ..models.server_status import ServerStatus

class Model:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str,
                 dir_name: str = OUTPUT_DIR_NAME) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)
        self.model_file = self.dir.joinpath(f'{prj_name}.tar.gz')
        self.training_data_file = self.dir.joinpath(TRAINING_DATA_FILE_NAME)
        # Tools
        self.yaml = YAML(typ='safe')
        # env var
        self.env_rasa_api_url = os.getenv("RASA_API_URL")
        self.env_asar_api_url = os.getenv("ASAR_API_URL")

    def init(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
    
    def check_health(self, rasa_api_url)-> bool:
        try:
            resp = requests.get(url=f'{rasa_api_url}')
            if resp.status_code == requests.codes.ok:
                return True
            else:
                return False
        except:
            return False

    def train(self, custom_rasa_api_url=None, custom_asar_api_url=None) -> None:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        asar_api_url = custom_asar_api_url or self.env_asar_api_url
        
        if rasa_api_url and asar_api_url:
            params = {'save_to_default_model_directory': 'false',
                    'force_training': 'true',
                    'callback_url': f'{asar_api_url}/projects/{self.prj_name}/models'}
            
            if self.check_health(rasa_api_url):
                server_status = ServerStatus.query.first()
                if self.prj_name == server_status.loaded_project:
                    resp = requests.delete(url=f'{rasa_api_url}/model')
                
                with open(self.training_data_file, 'r', encoding="utf-8") as f:
                    data = f.read()
                resp = requests.post(url=f'{rasa_api_url}/model/train',
                                        params=params,
                                        data=data.encode('utf-8'))
                return 200, resp.status_code, 'ok'
            else:
                return 400, None, 'Can not connect to Rasa API server.'
        else:
            return 400, None, 'Please provide RASA_API_URL and ASAR_API_URL.'

    def load(self, custom_rasa_api_url=None) -> None:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        
        if rasa_api_url:
            data = {'model_file': self.model_file.absolute().as_posix()}
            
            if self.check_health(rasa_api_url):
                resp = requests.put(url=f'{rasa_api_url}/model', 
                                        json=data,
                                        timeout=300)
                return 200, resp.status_code, 'ok'
            else:
                return 400, None, 'Can not connect to Rasa API server.'
        else:
            return 400, None, 'Please provide RASA_API_URL.'

    def save(self, content) -> None:
        with open(self.model_file, 'wb') as t:
            t.write(content)
