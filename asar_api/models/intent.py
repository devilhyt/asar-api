import re
from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel, validator, root_validator, conlist, constr
from ..config import INTENTS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Intent(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'examples': [{'text': 'default', 'labels':[]}]}
        super().__init__(prj_path=prj_path,
                         file_name=INTENTS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=IntentNameSchema,
                         object_schema=IntentObjectSchema)


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
    rule: Optional[str]
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