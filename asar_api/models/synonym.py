import re
from typing import Optional, List
from pathlib import Path
from pydantic import BaseModel, validator
from ..config import SYNONYMS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema
from ruamel.yaml.scalarstring import LiteralScalarString
from ..utils.utils import MyYAML

class Synonym(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'examples': []}
        super().__init__(prj_path=prj_path,
                         file_name=SYNONYMS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=SynonymNameSchema,
                         object_schema=SynonymObjectSchema)
        
    def compile(self) -> list:
        yaml = MyYAML()
        content:dict = self.content
        nlu = []

        for synonym_name, synonym in content.items():
            if examples := synonym["examples"]:
                nlu.append({'synonym': synonym_name,
                            'examples': LiteralScalarString(yaml.dump(examples))})
        return nlu

class SynonymNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if re.match(r"^\w+$", name) is None:
                raise ValueError({'msgCode':'invalidName', 'msg':'Invalid name.'})
        return name


class SynonymObjectSchema(BaseModel):
    examples: Optional[List[str]]
