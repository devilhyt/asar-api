from pathlib import Path
from wingman_api.config import (WINGMAN_PRJ_DIR, INTENTS_FILE_NAME, INTENT_KEYS, INTENT_KEYS_ADDED)
class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)
    def __init__(self, project_name):
        intents_file = self.prj_root.joinpath(project_name, 'intents', INTENTS_FILE_NAME)
        pass
    def test(self):
        print()