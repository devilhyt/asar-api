from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from wingman_api.config import ACTIONS_DIR_NAME, ACTIONS_FILE_NAME
from .file_basis import FileBasis


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=ACTIONS_DIR_NAME,
                         file_name=ACTIONS_FILE_NAME,
                         object_schema=ActionObjectSchema)


class ActionObjectSchema(BaseModel):
    action_type: str
    data: Optional[list]
