from pathlib import Path
from wingman_api.config import (
    STORIES_FILE_NAME, STORY_KEYS, STORY_KEYS_ADDED)
from .file_basis import FileBasis

class Story(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('stories', STORIES_FILE_NAME),
                         keys=STORY_KEYS + STORY_KEYS_ADDED)