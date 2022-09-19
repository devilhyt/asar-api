import re
from typing import Any, Optional, List, Literal
from pathlib import Path
from pydantic import BaseModel, validator, conlist
from ..config import SLOTS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Slot(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content={'type':'any'}
        super().__init__(prj_path=prj_path,
                         file_name=SLOTS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=SlotNameSchema,
                         object_schema=SlotObjectSchema)

class SlotNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^\w+$", name):
                raise ValueError('Invalid name')
        return name

class SlotConditionSchema(BaseModel):
    active_loop : str
    requested_slot: Optional[str]
    
class SlotMappingSchema(BaseModel):
    type: Literal['from_entity', 'from_text', 'from_intent', 'from_trigger_intent', 'custom']
    intent: Optional[Any]
    not_intent: Optional[Any]
    entity: Optional[str]
    role: Optional[str]
    group: Optional[str]
    value: Optional[Any]
    action: Optional[str]
    conditions: Optional[List[SlotConditionSchema]]
    

class SlotObjectSchema(BaseModel):
    type: Literal['text', 'bool' ,'categorical', 'float' ,'list', 'any']
    values: Optional[list]
    min_value: Optional[float]
    max_value: Optional[float]
    initial_value: Optional[Any]
    mappings: Optional[List[SlotMappingSchema]]
    
    
