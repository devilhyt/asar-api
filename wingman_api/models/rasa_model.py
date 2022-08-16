from pathlib import Path
import requests
import yaml
from wingman_api.config import MODELS_DIR_NAME, SERVER_URL, RASA_URL


class RasaModel:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str,
                 dir_name: str = MODELS_DIR_NAME) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)

    def init(self) -> None:
        self.dir.mkdir(parents=True)

    def train(self, rasa_url = f'{RASA_URL}/model/train'):
        params = {'save_to_default_model_directory': 'false',
                  'force_training': 'true',
                  'callback_url': f'{SERVER_URL}/projects/{self.prj_name}/models'}
        # Todo: generate yaml from this project
        with open('./test/test.yml', 'r') as f:
            data = yaml.safe_load(f)
        response = requests.post(url=rasa_url, params=params, data=yaml.dump(data))
        
        return response.status_code

    def load(self, rasa_url = f'{RASA_URL}/model'):
        data = {'model_file': f'{self.dir}/model.tar.gz'}
        response = requests.put(url=rasa_url, json=data)
        return response.status_code 
    
    def save(self, content):
        with open(f'{self.dir}/model.tar.gz', 'wb') as t:
            t.write(content)
            
    def convert_intent(self):
        ...
