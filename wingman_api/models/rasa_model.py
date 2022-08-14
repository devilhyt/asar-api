from typing import Optional
from pathlib import Path
from pydantic import BaseModel
import requests


class RasaModel:
    def __init__(self,
                 prj_name: str,
                 prj_path: Path,
                 dir_name: str) -> None:
        self.prj_name = prj_name
        self.dir = prj_path.joinpath(dir_name)

    def init(self) -> None:
        self.dir.mkdir(parents=True)

    def train(self, url):
        params = {"save_to_default_model_directory": "false", "force_training": "true"}
        ...

    def load(self, url) -> bool:
        data = {'model_file': f'{self.dir}/{self.prj_name}'}
        response = requests.put(url=url,
                                json=data)
        if response.status_code == requests.codes.ok:
            return True
        else:
            return False
