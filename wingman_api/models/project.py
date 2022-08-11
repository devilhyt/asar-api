import shutil
import re
from pathlib import Path
from pydantic import BaseModel, validator
from wingman_api.config import WINGMAN_PRJ_DIR, MODELS_DIR_NAME
from .intent import Intent
from .action import Action
from .entity import Entity
from .story import Story
from .rule import Rule
from .token import Token


class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)

    def __init__(self, project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=project_name)
        # Implement
        self.prj_root.mkdir(parents=True, exist_ok=True)
        self.prj_path = self.prj_root.joinpath(project_name)
        self.intent = Intent(self.prj_path)
        self.action = Action(self.prj_path)
        self.entity = Entity(self.prj_path)
        self.story = Story(self.prj_path)
        self.rule = Rule(self.prj_path)
        self.token = Token(self.prj_path)

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    def create(self) -> None:
        self.prj_path.mkdir(parents=True, exist_ok=False)
        self.intent.init()
        self.action.init()
        self.entity.init()
        self.story.init()
        self.rule.init()
        self.token.init()
        self.prj_path.joinpath(MODELS_DIR_NAME).mkdir()

    def rename(self, new_project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=new_project_name)
        # Implement
        target = self.prj_root.joinpath(new_project_name)
        self.prj_path.rename(target)

    def delete(self) -> None:
        shutil.rmtree(self.prj_path)


class ProjectNameSchema(BaseModel):
    name: str

    @validator('name')
    def check_name(cls, name: str):
        if not re.match(r"^\w+$", name):
            raise ValueError('Invalid name')
        return name
