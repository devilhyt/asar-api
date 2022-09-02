from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from ..config import STORIES_DIR_NAME, STORIES_FILE_NAME
from .file_basis import FileBasis


class Story(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         dir_name=STORIES_DIR_NAME,
                         file_name=STORIES_FILE_NAME,
                         object_schema=StoryObjectSchema)


class StoryObjectSchema(BaseModel):
    nodes: Optional[list]
    edges: Optional[list]
    position: Optional[list]
    zoom: Optional[int]
