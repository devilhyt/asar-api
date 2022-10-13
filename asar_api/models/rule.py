from pathlib import Path
from pydantic import BaseModel, Extra
from ..config import RULES_FILE_NAME
from .file_basis import FileBasis


class Rule(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         file_name=RULES_FILE_NAME,
                         object_schema=RuleObjectSchema)


class RuleObjectSchema(BaseModel, extra=Extra.allow):
    pass
