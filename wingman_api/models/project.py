from pathlib import Path
import shutil
from pydantic import BaseModel, validator
from wingman_api.config import (
    WINGMAN_PRJ_DIR, WINGMAN_PRJ_STRUCT)
from .intent import Intent
from .action import Action
from .story import Story


class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)

    def __init__(self, project_name) -> None:
        self.prj_root.mkdir(parents=True, exist_ok=True)
        self.prj_path = Path(WINGMAN_PRJ_DIR, project_name)
        self.intent = Intent(self.prj_path)
        self.action = Action(self.prj_path)
        self.story = Story(self.prj_path)

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    @staticmethod
    def create(project_name) -> None:
        prj_dir = Project.prj_root.joinpath(project_name)
        prj_dir.mkdir(parents=True)

        for dir, files in WINGMAN_PRJ_STRUCT.items():
            sub_dir = prj_dir.joinpath(dir)
            sub_dir.mkdir(parents=True)
            for f in files:
                sub_file = sub_dir.joinpath(f)
                sub_file.touch()
                if sub_file.suffix == '.json':
                    sub_file.write_text('{}')

    def rename(self, new_project_name) -> None:
        target = self.prj_root.joinpath(new_project_name)
        self.prj_path.rename(target)

    def delete(self) -> None:
        shutil.rmtree(self.prj_path)


class ProjectSchema(BaseModel):
    project_name: str

    @validator('*')
    def check_relpath(cls, v):
        """avoid relative path"""

        check_list = ['.', '/', '\\', ':']
        if any(elem in v for elem in check_list):
            raise ValueError('Cannot use relative path')
        return v


class ProjectSchemaUpdate(ProjectSchema):
    new_project_name: str
