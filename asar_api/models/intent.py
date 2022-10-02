import re
from typing import Optional, List, Tuple
from pathlib import Path
from pydantic import BaseModel, validator, root_validator, conlist, constr
from ..config import INTENTS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema
from ruamel.yaml.scalarstring import LiteralScalarString


class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'examples': [
            {'text': 'default', 'labels': []}]}
        super().__init__(prj_path=prj_path,
                         file_name=INTENTS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=IntentNameSchema,
                         object_schema=IntentObjectSchema)

    def compile(self) -> Tuple[list, dict]:
        content = self.content
        nlu = []
        domain = {'intents': []}

        for intent_name, intent in content.items():
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
            nlu.append({'intent': intent_name,
                        'examples': examples_arr})

            # domain
            intent.pop('examples')
            if intent:
                domain['intents'].append({intent_name: intent})
            else:
                domain['intents'].append(intent_name)

        return nlu, domain


class IntentNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^\w+/?\w+$", name):
                raise ValueError('Invalid name')
        return name


class IntentLabelSchema(BaseModel):
    token: str
    start: int
    end: int
    entity: str
    role: Optional[str]
    group: Optional[str]


class IntentExampleSchema(BaseModel):
    text: constr(min_length=1)
    metadata: Optional[dict]
    labels: Optional[List[IntentLabelSchema]]


class IntentObjectSchema(BaseModel):
    examples: conlist(IntentExampleSchema, min_items=1)
    use_entities: Optional[List[str]]
    ignore_entities: Optional[List[str]]

    @root_validator
    def check_use_ignore_entities(cls, values: dict):
        if values.get('use_entities') and values.get('ignore_entities'):
            raise ValueError(
                'You can only use_entities or ignore_entities for any single intent.')
        return values
