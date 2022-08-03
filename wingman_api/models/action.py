from pathlib import Path
from wingman_api.config import (
    ACTIONS_FILE_NAME, ACTION_KEYS, ACTION_KEYS_ADDED)
from .file_basis import FileBasis


class Action(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('actions', ACTIONS_FILE_NAME),
                         keys=ACTION_KEYS + ACTION_KEYS_ADDED)
