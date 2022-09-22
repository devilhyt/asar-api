import shutil
import re
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from pydantic import BaseModel, validator
from jinja2 import Template
from ..config import ASAR_PRJ_DIR, TRAINING_DATA_FILE_NAME, ACTIONS_PY_NAME, ASAR_TEMPLATES_DIR
from .intent import Intent
from .action import Action
from .entity import Entity
from .slot import Slot
from .story import Story
from .rule import Rule
from .token import Token
from .model import Model
from .lconfig import LConfig


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
        self.actions = Action(self.prj_path)
        self.entities = Entity(self.prj_path)
        self.slots = Slot(self.prj_path)
        self.stories = Story(self.prj_path)
        self.rules = Rule(self.prj_path)
        self.tokens = Token(self.prj_path)
        self.models = Model(self.prj_path, self.prj_name)
        self.lconfigs = LConfig(self.prj_path)
        # Tools
        self.yaml = YAML()

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
        self.lconfigs.init()

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
        domain = {'intents': [], 'entities': [], 'actions': []}

        # compile intents
        intents = self.intents.content
        for intent_name, intent in intents.items():
            # nlu
            examples_arr = []
            for example in intent['examples']:
                text = ''
                previous_end = 0
                sorted_labels = sorted(
                    example['labels'], key=lambda d: d['start'])
                for label in sorted_labels:
                    token = label.get('token')
                    entity = label.get('entity')
                    role = label.get('role')
                    group = label.get('group')
                    text += example['text'][previous_end:label['start']]
                    text += f'[{token}]'
                    text += f'{{'
                    text += f'"entity": "{entity}"'
                    if role:
                        text += f', "role": "{role}"'
                    if group:
                        text += f', "group": "{group}"'
                    text += f'}}'
                    previous_end = label['end']
                text += example['text'][previous_end:]
                text += '\n'
                examples_arr.append({'text': LiteralScalarString(text)})
            nlu['nlu'].append({'intent': intent_name,
                               'examples': examples_arr})

            # domain
            intent.pop('examples')
            if intent:
                domain['intents'].append({intent_name: intent})
            else:
                domain['intents'].append(intent_name)

        # compile entities
        entities = self.entities.content
        for entity_name, entity in entities.items():
            if entity:
                domain['entities'].append({entity_name: entity})
            else:
                domain['entities'].append(entity_name)

        # compile actions
        domain['actions'] = self.actions.names  # domain

        with open(f'{ASAR_TEMPLATES_DIR}/action.j2', 'r', encoding='utf-8') as j:  # py
            template = j.read()
        j2_template = Template(template)
        gen = j2_template.render(actions=self.actions.content)
        with open(file=self.models.dir.joinpath(ACTIONS_PY_NAME),
                  mode='w',
                  encoding="utf-8") as py:
            py.write(gen)

        # gen yaml
        training_data = nlu | domain
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
