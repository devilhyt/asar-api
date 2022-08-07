from typing import Optional
from pathlib import Path
from pydantic import BaseModel, conlist
from wingman_api.config import RULES_FILE_NAME
from .file_basis import FileBasis


class Rule(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('rules', RULES_FILE_NAME),
                         object_schema=RuleObjectSchema)


class RuleObjectSchema(BaseModel):
    nodes: Optional[conlist(dict, max_items=1)]
    edges: Optional[list]
    position: Optional[list]
    zoom: Optional[int]
