import re
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, validator, conlist
from ..config import FORMS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Form(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {}
        super().__init__(prj_path=prj_path,
                         file_name=FORMS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=FormNameSchema,
                         object_schema=FormObjectSchema)
    # def compile(self) -> dict:
    #     domain = {'slots': []}
    #     domain['slots'] = self.content
    #     return domain


class FormNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if re.match(r"^[A-Za-z0-9_]+$", name) is None:
                raise ValueError({'msgCode':'invalidName', 'msg':'Invalid name.'})
        return name


class FormObjectSchema(BaseModel):
    required_slots: Optional[list]
    ignored_intents: Optional[list]
