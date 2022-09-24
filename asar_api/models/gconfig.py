from typing import Optional
from pydantic import BaseModel, Field
import json
from ruamel.yaml import YAML
from pathlib import Path
from ..config import ASAR_DATA_ROOT, GCONFIG_FILE_NAME


class GConfig():
    def __init__(self) -> None:
        self.file = Path(ASAR_DATA_ROOT).joinpath(GCONFIG_FILE_NAME)
        self.object_schema = GConfigSchema
        # Tools
        self.yaml = YAML()

    @property
    def content(self) -> dict:
        return self.read_json()

    @property
    def names(self) -> tuple:
        return tuple(self.content.keys())

    def init(self) -> None:
        if not self.file.exists():
            self.file.touch()
            self.file.write_text(GConfigSchema().json(by_alias=True, indent=4))
            self.compile()

    def update(self, input_content) -> None:
        # Validate
        valid_content = self.object_schema.parse_obj(input_content)
        # Implement
        content = valid_content.dict(by_alias=True)
        self.write_json(content)
        self.compile()

    def compile(self) -> None:
        # Todo: optimize required
        content = self.content
        with open(file=Path(ASAR_DATA_ROOT).joinpath("credentials.yml"),
                  mode='w',
                  encoding="utf-8") as y:
            self.yaml.dump(data=content["credentials"], stream=y)
        with open(file=Path(ASAR_DATA_ROOT).joinpath("endpoints.yml"),
                  mode='w',
                  encoding="utf-8") as y:
            self.yaml.dump(data=content["endpoints"], stream=y)

    def read_json(self) -> dict:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_json = json.load(f)
        return f_json

    def write_json(self, f_json: dict) -> dict:
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(f_json, f, indent=4, ensure_ascii=False)


class DockerSchema(BaseModel):
    rasa_container: str = 'app'
    action_container: str = 'action'
    asar_api_url: str = 'http://localhost:5500'
    rasa_api_url: str = 'http://localhost:5005'


class RasaCredentialsSchema(BaseModel):
    url: str = "http://localhost:5002/api"


class TelegramCredentialsSchema(BaseModel):
    access_token: str
    verify: str
    webhook_url: str


class FacebookCredentialsSchema(BaseModel):
    verify: str
    secret: str
    page_access_token: str = Field(alias='page-access-token')


class CredentialsSchema(BaseModel):
    rest: None = None
    rasa: RasaCredentialsSchema = RasaCredentialsSchema()
    telegram: Optional[TelegramCredentialsSchema]
    facebook: Optional[FacebookCredentialsSchema]


class ActionEndpointSchema(BaseModel):
    url: str = "http://localhost:5055/webhook"


class EndpointsSchema(BaseModel):
    action_endpoint: ActionEndpointSchema = ActionEndpointSchema()


class GConfigSchema(BaseModel):
    docker: DockerSchema = DockerSchema()
    credentials: CredentialsSchema = CredentialsSchema()
    endpoints: EndpointsSchema = EndpointsSchema()