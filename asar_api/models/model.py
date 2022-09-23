from pathlib import Path
import requests
from ruamel.yaml import YAML
from ..config import OUTPUT_DIR_NAME, MODELS_FILE_NAME


class Model:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str,
                 dir_name: str = OUTPUT_DIR_NAME,
                 file_name: str = MODELS_FILE_NAME) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)
        self.file = self.dir.joinpath(file_name)
        # Tools
        self.yaml = YAML(typ='safe')

    def init(self) -> None:
        self.dir.mkdir(parents=True)

    def train(self, rasa_api_url, asar_api_url) -> None:
        params = {'save_to_default_model_directory': 'false',
                  'force_training': 'true',
                  'callback_url': f'{asar_api_url}/projects/{self.prj_name}/models'}
        # Todo: generate yaml from this project
        with open('./test/test.yml', 'r', encoding="utf-8") as f:
            data = f.read()
        response = requests.post(url=f'{rasa_api_url}/model/train',
                                 params=params,
                                 data=data)

        return response.status_code

    def load(self, rasa_api_url) -> None:
        data = {'model_file': self.file.absolute().as_posix()}
        response = requests.put(url=f'{rasa_api_url}/model', json=data)
        return response.status_code

    def save(self, content) -> None:
        with open(self.file, 'wb') as t:
            t.write(content)
