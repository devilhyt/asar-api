from pathlib import Path
import json
import shutil
from wingman_api.config import (
    WINGMAN_PRJ_DIR, WINGMAN_PRJ_STRUCT,
    INTENTS_FILE_NAME, INTENT_KEYS, INTENT_KEYS_ADDED,
    ACTIONS_FILE_NAME, ACTION_KEYS, ACTION_KEYS_ADDED)


class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)

    def __init__(self, project_name) -> None:
        self.prj_root.mkdir(parents=True, exist_ok=True)
        Project.check_relpath(project_name)
        self.prj_path = Path(WINGMAN_PRJ_DIR, project_name)
        self.intent = Intent(self.prj_path)
        self.action = Action(self.prj_path)

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    @staticmethod
    def create(project_name) -> None:
        Project.check_relpath(project_name)
        prj_dir = Project.prj_root.joinpath(project_name)
        prj_dir.mkdir(parents=True)

        for dir, files in WINGMAN_PRJ_STRUCT.items():
            sub_dir = prj_dir.joinpath(dir)
            sub_dir.mkdir(parents=True)
            for f in files:
                sub_file = sub_dir.joinpath(f)
                sub_file.touch()
                if sub_file.suffix == '.json':
                    sub_file.write_text('{}')

    def rename(self, new_project_name) -> None:
        Project.check_relpath(new_project_name)
        target = self.prj_root.joinpath(new_project_name)
        self.prj_path.rename(target)

    def delete(self) -> None:
        shutil.rmtree(self.prj_path)

    @staticmethod
    def check_relpath(name: str):
        """avoid relative path"""

        check_list = ['..', '/', '\\', ':']
        if any(elem in name for elem in check_list):
            raise ValueError('Cannot use relative path')


class FileBasis():
    def __init__(self, file: Path, keys: list) -> None:
        self.file = file
        self.keys = keys

    @property
    def content(self) -> dict:
        return self.read_json()

    @property
    def names(self) -> tuple:
        return tuple(self.content.keys())

    def create(self, name: str, input_content: dict = {}) -> None:
        # Validity check
        self.check_key(input_content)
        if name is None:
            raise ValueError(f'Missing {self.__class__.__name__} Name')
        content = self.content
        if name in content:
            raise ValueError(f'{self.__class__.__name__} already exist')

        # Implement
        content[name] = input_content
        self.write_json(content)

    def update(self, name, new_name, input_content) -> None:
        # Validity check
        self.check_key(input_content)
        content = self.content
        if name not in content:
            raise ValueError(f'{self.__class__.__name__} does not exist')
        elif new_name:
            if new_name in content:
                raise ValueError('Duplicate names are not allowed')

        # Implement
        if input_content:
            content[name] = input_content
        if new_name:
            content[new_name] = content.pop(name)
        self.write_json(content)

    def delete(self, name) -> None:
        content = self.content
        del content[name]
        self.write_json(content)

    def read_json(self) -> dict:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_json = json.load(f)
        return f_json

    def write_json(self, f_json: dict) -> dict:
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(f_json, f, indent=4)

    def check_key(self, content: dict):
        """avoid invalid keys"""
        if any(key not in self.keys for key in content):
            raise ValueError('Invalid Key')


class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('intents', INTENTS_FILE_NAME),
                         keys=INTENT_KEYS + INTENT_KEYS_ADDED)


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('actions', ACTIONS_FILE_NAME),
                         keys=ACTION_KEYS + ACTION_KEYS_ADDED)
