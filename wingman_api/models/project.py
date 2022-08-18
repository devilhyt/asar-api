import shutil
import re
from pathlib import Path
from pydantic import BaseModel, validator
from wingman_api.config import WINGMAN_PRJ_DIR
from .intent import Intent
from .action import Action
from .entity import Entity
from. slot import Slot
from .story import Story
from .rule import Rule
from .token import Token
from .model import Model


class Project:
    prj_root = Path(WINGMAN_PRJ_DIR)

    def __init__(self, project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=project_name)
        # Implement
        self.prj_name = project_name
        self.prj_root.mkdir(parents=True, exist_ok=True)
        self.prj_path = self.prj_root.joinpath(project_name)
        self.intents = Intent(self.prj_path)
        self.actions = Action(self.prj_path)
        self.entities = Entity(self.prj_path)
        self.slots = Slot(self.prj_path)
        self.stories = Story(self.prj_path)
        self.rules = Rule(self.prj_path)
        self.tokens = Token(self.prj_path)
        self.models = Model(self.prj_path, self.prj_name)

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    def create(self) -> None:
        self.prj_path.mkdir(parents=True, exist_ok=False)
        self.intents.init()
        self.actions.init()
        self.entities.init()
        self.slots.init()
        self.stories.init()
        self.rules.init()
        self.tokens.init()
        self.models.init()

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
