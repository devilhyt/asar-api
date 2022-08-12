import re
from typing import Any, List, Optional
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

class ActionResponseButtonSchema(BaseModel):
    title: str
    payload: str

class ActionResponseConditionSchema(BaseModel):
    type: str
    name: str
    value: Any

class ActionResponseSchema(BaseModel):
    text: Optional[str]
    image: Optional[str]
    button: Optional[List[ActionResponseButtonSchema]]
    button_type: Optional[str]
    quick_replies: Optional[List[ActionResponseButtonSchema]]
    attachment: Optional[str]
    elements: Optional[List[dict]]
    channel: Optional[str]
    metadata: Optional[dict]
    condition: Optional[List[ActionResponseConditionSchema]]

class ActionObjectSchema(BaseModel):
    action_type: str
    data: Optional[List[ActionResponseSchema]]
