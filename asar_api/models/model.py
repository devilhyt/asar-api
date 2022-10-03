from pathlib import Path
import requests
from ruamel.yaml import YAML
from ..config import OUTPUT_DIR_NAME
import os


class Model:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str,
                 dir_name: str = OUTPUT_DIR_NAME) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)
        self.file = self.dir.joinpath(f'{prj_name}.tar.gz')
        # Tools
        self.yaml = YAML(typ='safe')
        # env var
        self.env_rasa_api_url = os.getenv("RASA_API_URL")
        self.env_asar_api_url = os.getenv("ASAR_API_URL")

    def init(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)

    def train(self, custom_rasa_api_url=None, custom_asar_api_url=None) -> None:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        asar_api_url = custom_asar_api_url or self.env_asar_api_url
        
        if rasa_api_url and asar_api_url:
            params = {'save_to_default_model_directory': 'false',
                    'force_training': 'true',
                    'callback_url': f'{asar_api_url}/projects/{self.prj_name}/models'}
            
            # response = requests.get(url=f'{rasa_api_url}/status')
            # if response.json().get("num_active_training_jobs") > 0:
            #     return 400, "Still training"
            # resp = requests.get(url=f'{rasa_api_url}')
            # if resp.status_code != requests.codes.ok:
            #     return resp.status_code

            # Todo: generate yaml from this project
            with open('./test/test.yml', 'r', encoding="utf-8") as f:
                data = f.read()
            response = requests.post(url=f'{rasa_api_url}/model/train',
                                    params=params,
                                    data=data)
            return 200, response.status_code, ""
        else:
            return 400, None, "Please provide RASA_API_URL and ASAR_API_URL."

    def load(self, custom_rasa_api_url=None) -> None:
        rasa_api_url = custom_rasa_api_url or self.env_rasa_api_url
        
        if rasa_api_url:
            data = {'model_file': self.file.absolute().as_posix()}
            response = requests.put(url=f'{rasa_api_url}/model', 
                                    json=data,
                                    timeout=300)
            return 200, response.status_code, ""
        else:
            return 400, None, "Please provide RASA_API_URL."

    def save(self, content) -> None:
        with open(self.file, 'wb') as t:
            t.write(content)
