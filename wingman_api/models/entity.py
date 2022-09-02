import re
from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import ENTITIES_DIR_NAME, ENTITIES_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Entity(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=ENTITIES_DIR_NAME,
                         file_name=ENTITIES_FILE_NAME,
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
