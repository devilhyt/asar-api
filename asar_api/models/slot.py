import re
from typing import Any, Optional, List, Literal, Union
from pathlib import Path
from pydantic import BaseModel, validator, Field, conlist
from ..config import SLOTS_FILE_NAME
from .file_basis import FileBasis, GeneralNameSchema


class Slot(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        self.default_content = {'influence_conversation': False,
                                'type': 'any',
                                'mappings':[{'type':'custom'}]}
        super().__init__(prj_path=prj_path,
                         file_name=SLOTS_FILE_NAME,
                         default_content=self.default_content,
                         name_schema=SlotNameSchema,
                         object_schema=SlotObjectSchema)
    def compile(self) -> dict:
        domain = {'slots': []}
        domain['slots'] = self.content
        return domain

class SlotNameSchema(GeneralNameSchema):
    @validator('*')
    def check_name(cls, name: str):
        if name:
            if not re.match(r"^[A-Za-z0-9_]+$", name):
                raise ValueError('Invalid name')
        return name


class SlotConditionSchema(BaseModel):
    active_loop: str
    requested_slot: Optional[str]


# class SlotMappingSchema(BaseModel):
#     type: Literal['from_entity', 'from_text',
#                   'from_intent', 'from_trigger_intent', 'custom']
#     intent: Optional[Any]
#     not_intent: Optional[Any]
#     entity: Optional[str]
#     role: Optional[str]
#     group: Optional[str]
#     value: Optional[Any]
#     action: Optional[str]
#     conditions: Optional[List[SlotConditionSchema]]


# class SlotObjectSchema(BaseModel):
#     influence_conversation: Optional[bool]
#     type: Literal['text', 'bool', 'categorical', 'float', 'list', 'any']
#     values: Optional[list]
#     min_value: Optional[float]
#     max_value: Optional[float]
#     initial_value: Optional[Any]
#     mappings: Optional[List[SlotMappingSchema]]


class SlotCondition(BaseModel):
    active_loop: str
    requested_slot: Optional[str]


class SlotMappingBase(BaseModel):
    conditions: Optional[List[SlotCondition]]


class SlotMappingEntity(SlotMappingBase):
    type: Literal['from_entity']
    intent: Optional[Any]
    not_intent: Optional[Any]
    entity: Optional[str]
    role: Optional[str]
    group: Optional[str]


class SlotMappingText(SlotMappingBase):
    type: Literal['from_text']
    intent: Optional[Any]
    not_intent: Optional[Any]


class SlotMappingIntent(SlotMappingBase):
    type: Literal['from_intent']
    intent: Optional[Any]
    not_intent: Optional[Any]
    value: Optional[Any]


class SlotMappingTriggerIntent(SlotMappingBase):
    type: Literal['from_trigger_intent']
    intent: Optional[Any]
    not_intent: Optional[Any]
    value: Optional[Any]


class SlotMappingCustom(SlotMappingBase):
    type: Literal['custom']
    action: Optional[str]


class SlotMappingSchema(BaseModel):
    __root__: Union[SlotMappingEntity,
                    SlotMappingText,
                    SlotMappingIntent,
                    SlotMappingTriggerIntent,
                    SlotMappingCustom] = Field(..., discriminator='type')


class SlotTypeBase(BaseModel):
    influence_conversation: Optional[bool]
    initial_value: Optional[Any]
    mappings: conlist(SlotMappingSchema, min_items=1)


class SlotTypeText(SlotTypeBase):
    type: Literal['text']


class SlotTypeBool(SlotTypeBase):
    type: Literal['bool']


class SlotTypeCategorical(SlotTypeBase):
    type: Literal['categorical']
    values: Optional[list]


class SlotTypeFloat(SlotTypeBase):
    type: Literal['float']
    min_value: Optional[float]
    max_value: Optional[float]


class SlotTypeList(SlotTypeBase):
    type: Literal['list']


class SlotTypeAny(SlotTypeBase):
    type: Literal['any']

    @validator('influence_conversation')
    def check_influence_conversation(cls, i):
        return False


class SlotObjectSchema(BaseModel):
    __root__: Union[SlotTypeText,
                    SlotTypeBool,
                    SlotTypeCategorical,
                    SlotTypeFloat,
                    SlotTypeList,
                    SlotTypeAny] = Field(..., discriminator='type')
