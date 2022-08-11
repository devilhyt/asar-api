import re
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, validator
from wingman_api.config import ACTIONS_DIR_NAME, ACTIONS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=ACTIONS_DIR_NAME,
                         file_name=ACTIONS_FILE_NAME,
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
    action_type: str
    data: Optional[list]
