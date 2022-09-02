from typing import Optional
from pathlib import Path
from pydantic import BaseModel, conlist
from ..config import RULES_DIR_NAME, RULES_FILE_NAME
from .file_basis import FileBasis


class Rule(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=RULES_DIR_NAME,
                         file_name=RULES_FILE_NAME,
                         object_schema=RuleObjectSchema)


class RuleObjectSchema(BaseModel):
    nodes: Optional[conlist(dict, max_items=1)]
    edges: Optional[list]
    position: Optional[list]
    zoom: Optional[int]
