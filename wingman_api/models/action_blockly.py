import re
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, validator
from wingman_api.config import ACTIONS_DIR_NAME, ACTIONS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content={}
        super().__init__(prj_path=prj_path,
                         dir_name=ACTIONS_DIR_NAME,
                         file_name=ACTIONS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=ActionNameSchema,
                         object_schema=ActionObjectSchema)


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
