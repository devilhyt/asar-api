# from typing import Optional
from pydantic import BaseModel, Field
import json
# from ruamel.yaml import YAML
from pathlib import Path
from ..config import ASAR_DATA_ROOT, GCONFIG_FILE_NAME
# import docker


class GConfig():
    def __init__(self) -> None:
        self.file = Path(ASAR_DATA_ROOT).joinpath(GCONFIG_FILE_NAME)
        self.object_schema = GConfigSchema
        self.default_content = {
            "docker": {
                "rasa_container": "app",
                "action_container": "action"
            },
            # "credentials": {
            #     "rest": None,
            #     "rasa": {
            #         "url": "http://localhost:5002/api"
            #     }
            # },
            # "endpoints": {
            #     "action_endpoint": {
            #         "url": "http://localhost:5055/webhook"
            #     }
            # }
        }
        # Tools
        # self.yaml = YAML()
        # self.docker_client = docker.from_env()

    @property
    def content(self) -> dict:
        return self.read_json()

    @property
    def names(self) -> tuple:
        # not yet been used
        return tuple(self.content.keys())

    def init(self) -> None:
        if not self.file.exists():
            valid_content = self.object_schema.parse_obj(self.default_content)
            content = valid_content.dict(by_alias=True, exclude_unset=True)
            self.write_json(content)
            # TODO: optimize required
            # self.compile()

    def update(self, input_content) -> None:
        # Validate
        valid_content = self.object_schema.parse_obj(input_content)
        # Implement
        content = valid_content.dict(by_alias=True, exclude_unset=True)
        self.write_json(content)
        # TODO: optimize required
        # self.compile()

    # def compile(self) -> None:
    #     # TODO: optimize required
    #     content = self.content
    #     with open(file=Path(ASAR_DATA_ROOT).joinpath('credentials.yml'),
    #               mode='w',
    #               encoding="utf-8") as y:
    #         self.yaml.dump(data=content['credentials'], stream=y)
    #     with open(file=Path(ASAR_DATA_ROOT).joinpath('endpoints.yml'),
    #               mode='w',
    #               encoding="utf-8") as y:
    #         self.yaml.dump(data=content['endpoints'], stream=y)
    #     # docker
    #     container = self.docker_client.containers.get(
    #         content['docker']['rasa_container'])
    #     container.restart()

    def read_json(self) -> dict:
        with open(self.file, 'r', encoding="utf-8") as f:
            f_json = json.load(f)
        return f_json

    def write_json(self, f_json: dict) -> dict:
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(f_json, f, indent=4, ensure_ascii=False)


class DockerSchema(BaseModel):
    rasa_container: str
    action_container: str


# class RasaCredentialsSchema(BaseModel):
#     url: str


# class TelegramCredentialsSchema(BaseModel):
#     access_token: str
#     verify: str
#     webhook_url: str


# class FacebookCredentialsSchema(BaseModel):
#     verify: str
#     secret: str
#     page_access_token: str = Field(alias='page-access-token')


# class CredentialsSchema(BaseModel):
#     rest: None
#     rasa: RasaCredentialsSchema
#     telegram: Optional[TelegramCredentialsSchema]
#     facebook: Optional[FacebookCredentialsSchema]


# class ActionEndpointSchema(BaseModel):
#     url: str


# class EndpointsSchema(BaseModel):
#     action_endpoint: ActionEndpointSchema


class GConfigSchema(BaseModel):
    docker: DockerSchema
    # credentials: CredentialsSchema
    # endpoints: EndpointsSchema
