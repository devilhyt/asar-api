from pathlib import Path
from wingman_api.config import ACTIONS_FILE_NAME
from .file_basis import FileBasis
from pydantic import BaseModel
from typing import Optional


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('actions', ACTIONS_FILE_NAME),
                         object_schema=ActionObjectSchema)


class ActionObjectSchema(BaseModel):
    action_type: str
    data: Optional[list]
