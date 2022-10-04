import shutil
import re
from pathlib import Path
from ruamel.yaml import YAML
from pydantic import BaseModel, validator
from ..config import ASAR_PRJ_DIR, TRAINING_DATA_FILE_NAME
from .intent import Intent
from .action import Action
from .entity import Entity
from .slot import Slot
from .story import Story
from .rule import Rule
from .token import Token
from .model import Model
from .lconfig import LConfig
from .responese import Response
from .synonym import Synonym


class Project:
    prj_root = Path(ASAR_PRJ_DIR)

    def __init__(self, project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=project_name)
        # Implement
        self.prj_name = project_name
        self.prj_root.mkdir(parents=True, exist_ok=True)
        self.prj_path = self.prj_root.joinpath(project_name)
        self.intents = Intent(self.prj_path)
        self.responses = Response(self.prj_path)
        self.actions = Action(self.prj_path)
        self.entities = Entity(self.prj_path)
        self.slots = Slot(self.prj_path)
        self.stories = Story(self.prj_path)
        self.rules = Rule(self.prj_path)
        self.tokens = Token(self.prj_path)
        self.models = Model(self.prj_path, self.prj_name)
        self.lconfigs = LConfig(self.prj_path)
        self.synonyms = Synonym(self.prj_path)
        # Tools
        self.yaml = YAML()

    @staticmethod
    def names() -> tuple:
        return tuple([d.stem for d in Project.prj_root.iterdir() if d.is_dir()])

    def create(self) -> None:
        self.prj_path.mkdir(parents=True, exist_ok=False)
        self.intents.init()
        self.responses.init()
        self.actions.init()
        self.entities.init()
        self.slots.init()
        self.stories.init()
        self.rules.init()
        self.tokens.init()
        self.models.init()
        self.lconfigs.init(self.tokens.jieba_dir_path)
        self.synonyms.init()

    def rename(self, new_project_name) -> None:
        # Validate
        _ = ProjectNameSchema(name=new_project_name)
        # Implement
        target = self.prj_root.joinpath(new_project_name)
        self.prj_path.rename(target)

    def delete(self) -> None:
        shutil.rmtree(self.prj_path)

    def compile(self) -> None:
        nlu = {'nlu': []}
        domain = {'intents': [], 'entities': [], 'actions': [], 'slots':{}}
        stories = {}

        intents_nlu, intents_domain = self.intents.compile()
        nlu['nlu'] += intents_nlu
        domain.update(intents_domain)
        
        entities_domain = self.entities.compile()
        domain.update(entities_domain)
        
        actions_domain = self.actions.compile()
        domain.update(actions_domain)
        
        slots_domain = self.slots.compile()
        domain.update(slots_domain)
        
        compiled_stories = self.stories.compile()
        stories.update(compiled_stories)

        # gen yaml
        training_data = nlu | domain | stories
        with open(file=self.models.dir.joinpath(TRAINING_DATA_FILE_NAME),
                  mode='w',
                  encoding="utf-8") as y:
            self.yaml.dump(data=training_data, stream=y)

        # gen jieba dict
        self.tokens.gen_jieba_dict()


class ProjectNameSchema(BaseModel):
    name: str

    @validator('name')
    def check_name(cls, name: str):
        if not re.match(r"^\w+$", name):
            raise ValueError('Invalid name')
        return name
