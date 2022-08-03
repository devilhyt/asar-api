from pathlib import Path
import json

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
