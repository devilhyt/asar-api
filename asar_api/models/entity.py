import re
from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import ENTITIES_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Entity(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'roles': [], 'groups':[]}
        super().__init__(prj_path=prj_path,
                         file_name=ENTITIES_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=EntityNameSchema,
                         object_schema=EntityObjectSchema)

class EntityNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^\w+$", name):
                raise ValueError('Invalid name')
        return name

class EntityObjectSchema(BaseModel):
    roles: Optional[List[str]]
    groups: Optional[List[str]]
