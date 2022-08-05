from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from wingman_api.config import STORIES_FILE_NAME
from .file_basis import FileBasis


class Story(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('stories', STORIES_FILE_NAME),
                         object_schema=StoryObjectSchema)


class StoryObjectSchema(BaseModel):
    nodes: Optional[list]
    edges: Optional[list]
    position: Optional[list]
    zoom: Optional[int]
