import shutil
from pathlib import Path
from ruamel.yaml import YAML
from ..config import LCONFIG_FILE_NAME, ASAR_TEMPLATES_DIR


class LConfig():
    def __init__(self,
                 prj_path: Path) -> None:
        self.file = prj_path.joinpath(LCONFIG_FILE_NAME)
        # Tools
        self.yaml = YAML()

    @property
    def content(self) -> str:
        return self.read_file()

    def init(self, jieba_dir_path:Path) -> None:
        shutil.copy(f'{ASAR_TEMPLATES_DIR}/{LCONFIG_FILE_NAME}', self.file)

        data = self.yaml.load(self.content)
        data['pipeline'][0].update({'dictionary_path': str(jieba_dir_path.resolve())})
        with open(file=self.file, mode='w', encoding="utf-8") as y:
            self.yaml.dump(data=data, stream=y)

    def update(self, input_content) -> None:
        self.write_file(input_content)

    def read_file(self) -> str:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_str = f.read()
        return f_str

    def write_file(self, f_str: str) -> str:
        with open(self.file, 'w', encoding="utf-8") as f:
            f.write(f_str)
