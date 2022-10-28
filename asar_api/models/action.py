import re
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import (ACTIONS_FILE_NAME,
                      ASAR_TEMPLATES_DIR,
                      ACTIONS_PY_NAME,
                      OUTPUT_DIR_NAME,
                      ACTIONS_J2_NAME)
from .file_basis import FileBasis, GeneralNameSchema
from jinja2 import FileSystemLoader, Environment


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {}
        super().__init__(prj_path=prj_path,
                         file_name=ACTIONS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=ActionNameSchema,
                         object_schema=ActionObjectSchema)
        self.action_py_file = self.prj_path.joinpath(
            OUTPUT_DIR_NAME, ACTIONS_PY_NAME)
        self.builtin_names = ['action_listen',
                              'action_restart',
                              'action_session_start',
                              'action_default_fallback', 
                              'action_deactivate_loop',
                              'action_two_stage_fallback',
                              'action_default_ask_affirmation',
                              'action_default_ask_rephrase',
                              'action_back',
                              'action_unlikely_intent', 
                              'action_extract_slots',
                              'action_validate_slot_mappings']

    def compile(self) -> dict:
        domain = {'actions': []}
        domain['actions'] = self.names

        template_env = Environment(loader=FileSystemLoader(ASAR_TEMPLATES_DIR))
        template = template_env.get_template(ACTIONS_J2_NAME)
        rendered = template.render(actions=self.content)
        with open(file=self.action_py_file,
                  mode='w',
                  encoding="utf-8") as py:
            py.write(rendered)
        return domain


class ActionNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if re.match(r"^\w+/?\w+$", name) is None:
                raise ValueError({'msgCode':'invalidName', 'msg':'Invalid name.'})
        return name


class ActionObjectSchema(BaseModel):
    blockly: Optional[dict]
    packages: Optional[List[str]]
    code: Optional[str]
