import re
from typing import Any, List, Optional
from pathlib import Path
from pydantic import BaseModel, validator, root_validator, conlist
from ..config import RESPONSES_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Response(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'data': [{'text': 'default'}]}
        super().__init__(prj_path=prj_path,
                         file_name=RESPONSES_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=ResponseNameSchema,
                         object_schema=ResponseObjectSchema)

    def compile(self) -> dict:
        content = self.content
        domain = {'responses': {}}

        for response_name, response in content.items():
            domain['responses'].update({f'utter_{response_name}': response['data']})

        return domain


class ResponseNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if re.match(r"^\w+/?\w+$", name) is None:
                raise ValueError({'msgCode':'invalidName', 'msg':'Invalid name.'})
        return name


class ResponseButtonSchema(BaseModel):
    title: str
    payload: str


class ResponseConditionSchema(BaseModel):
    type: str
    name: str
    value: Any


class ResponseSchema(BaseModel):
    text: Optional[str]
    image: Optional[str]
    button: Optional[List[ResponseButtonSchema]]
    button_type: Optional[str]
    quick_replies: Optional[List[ResponseButtonSchema]]
    attachment: Optional[str]
    elements: Optional[List[dict]]
    channel: Optional[str]
    metadata: Optional[dict]
    condition: Optional[List[ResponseConditionSchema]]

    @root_validator
    def check_required(cls, values: dict):
        if values.get('text') or values.get('image') or values.get('button'):
            return values
        raise ValueError('Required one of text, image or button')


class ResponseObjectSchema(BaseModel):
    data: conlist(ResponseSchema, min_items=1)
