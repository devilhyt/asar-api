from pathlib import Path
from pydantic import BaseModel, Extra
from ..config import STORIES_FILE_NAME
from .file_basis import FileBasis


class Story(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         file_name=STORIES_FILE_NAME,
                         object_schema=StoryObjectSchema)


class StoryObjectSchema(BaseModel, extra=Extra.allow):
    pass
