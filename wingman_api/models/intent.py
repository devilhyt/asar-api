from pathlib import Path
from wingman_api.config import (
    INTENTS_FILE_NAME, INTENT_KEYS, INTENT_KEYS_ADDED)
from .file_basis import FileBasis

class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path.joinpath('intents', INTENTS_FILE_NAME),
                         keys=INTENT_KEYS + INTENT_KEYS_ADDED)