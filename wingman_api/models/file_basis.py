import json
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, validator


class GeneralNameSchema(BaseModel):
    name: str
    new_name: Optional[str]

    @validator('*')
    def check_name(cls, v) -> str:
        check_list = ['.', ' ', '\\', ':']
        if v and any(elem in v for elem in check_list):
            raise ValueError('Invalid name')
        return v


class GeneralObjectSchema(BaseModel):
    pass


class FileBasis():
    def __init__(self,
                 prj_path: Path,
                 dir_name: str,
                 file_name: str,
                 name_schema=GeneralNameSchema,
                 object_schema=GeneralObjectSchema) -> None:
        self.dir = prj_path.joinpath(dir_name)
        self.file = self.dir.joinpath(file_name)
        self.name_schema = name_schema
        self.object_schema = object_schema

    @property
    def content(self) -> dict:
        return self.read_json()

    @property
    def names(self) -> tuple:
        return tuple(self.content.keys())
    
    def init(self) -> None:
        self.dir.mkdir(parents=True)
        self.file.touch()
        self.file.write_text('{}')

    def get(self, name: str):
        # Validate
        _ = self.name_schema(name=name)
        # Implement
        return self.content[name]

    def create(self, name: str, input_content: dict = {}) -> None:
        # Validate
        _ = self.name_schema(name=name)
        _ = self.object_schema(**input_content)
        content = self.content
        if name in content:
            raise ValueError(f'{self.__class__.__name__} already exist')
        # Implement
        content[name] = input_content
        self.write_json(content)

    def update(self, name, new_name, input_content) -> None:
        # Validate
        _ = self.name_schema(name=name, new_name=new_name)
        if input_content:
            _ = self.object_schema(**input_content)
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
        # Validate
        _ = self.name_schema(name=name)
        # Implement
        content = self.content
        del content[name]
        self.write_json(content)

    def read_json(self) -> dict:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_json = json.load(f)
        return f_json

    def write_json(self, f_json: dict) -> dict:
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(f_json, f, indent=4, ensure_ascii=False)
