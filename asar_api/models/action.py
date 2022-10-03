import re
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import ACTIONS_FILE_NAME, ASAR_TEMPLATES_DIR, ACTIONS_PY_NAME, OUTPUT_DIR_NAME
from .file_basis import FileBasis, GeneralNameSchema
from jinja2 import Template


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {}
        super().__init__(prj_path=prj_path,
                         file_name=ACTIONS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=ActionNameSchema,
                         object_schema=ActionObjectSchema)
        self.action_py_file = self.prj_path.joinpath(OUTPUT_DIR_NAME, ACTIONS_PY_NAME)

    def compile(self) -> dict:
        domain = {'actions': []}
        domain['actions'] = self.names

        with open(f'{ASAR_TEMPLATES_DIR}/action.j2', 'r', encoding='utf-8') as j:  # py
            template = j.read()
        j2_template = Template(template)
        gen = j2_template.render(actions=self.content)
        with open(file=self.action_py_file,
                  mode='w',
                  encoding="utf-8") as py:
            py.write(gen)

        return domain


class ActionNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^\w+/?\w+$", name):
                raise ValueError('Invalid name')
        return name


class ActionObjectSchema(BaseModel):
    blockly: Optional[dict]
    packages: Optional[List[str]]
    code: Optional[str]
