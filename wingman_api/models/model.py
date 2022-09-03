from pathlib import Path
import requests
import yaml
from ..config import OUTPUT_DIR_NAME, MODELS_FILE_NAME, SERVER_URL, RASA_URL


class Model:
    def __init__(self,
                 prj_path: Path,
                 prj_name: str,
                 dir_name: str = OUTPUT_DIR_NAME,
                 file_name: str = MODELS_FILE_NAME) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)
        self.file = self.dir.joinpath(file_name)

    def init(self) -> None:
        self.dir.mkdir(parents=True)

    def train(self, rasa_url=RASA_URL) -> None:
        params = {'save_to_default_model_directory': 'false',
                  'force_training': 'true',
                  'callback_url': f'{SERVER_URL}/projects/{self.prj_name}/models'}
        # Todo: generate yaml from this project
        with open('./test/test.yml', 'r') as f:
            data = yaml.safe_load(f)
        response = requests.post(url=f'{rasa_url}/model/train',
                                 params=params,
                                 data=yaml.dump(data))

        return response.status_code

    def load(self, rasa_url=RASA_URL) -> None:
        data = {'model_file': self.file.absolute().as_posix()}
        response = requests.put(url=f'{rasa_url}/model', json=data)
        return response.status_code

    def save(self, content) -> None:
        with open(self.file, 'wb') as t:
            t.write(content)
