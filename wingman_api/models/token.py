from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel
from wingman_api.config import TOKENS_FILE_NAME
from .file_basis import FileBasis


class Token(FileBasis):
    def __init__(self, prj_path: Path) -> None:
    #     super().__init__(prj_path.joinpath('tokens', TOKENS_FILE_NAME),
    #                      object_schema=TokenObjectSchema)
        ...


class TokenObjectSchema(BaseModel):
    ...
