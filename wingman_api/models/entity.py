from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel
from wingman_api.config import ENTITIES_DIR_NAME, ENTITIES_FILE_NAME
from .file_basis import FileBasis


class Entity(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=ENTITIES_DIR_NAME,
                         file_name=ENTITIES_FILE_NAME,
                         object_schema=EntityObjectSchema)


class EntityObjectSchema(BaseModel):
    roles: Optional[List[str]]
    groups: Optional[List[str]]
