from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from ..models.project import Project
from ..models.file_basis import FileBasis
from ..models.intent import Intent
from ..models.action import Action
from ..models.entity import Entity
from ..models.slot import Slot
from ..models.story import Story
from ..models.rule import Rule
from typing import Union

file_types = Union[FileBasis, Intent, Action,
                   Entity, Entity, Slot, Story, Rule]


class ApiBasis(MethodView):
    """Asar API"""
    decorators = [jwt_required()]

    def __init__(self, attr_name: str) -> None:
        self.attr_name = attr_name

    def get(self, project_name, name):
        """Get objects
        :param name:
            If name is None, then return all objects.\n
            Else, then return an object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        if name:
            r = objs.select(name)
        elif mode == 'name':
            r = objs.names
        elif mode == 'builtin':
            r = getattr(objs, 'builtin_names', [])
        elif mode == 'schema':
            r = objs.object_schema.schema_json()
        else:
            r = objs.content
        return jsonify(r), 200

    def post(self, project_name):
        """Create an object"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', None)
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        status_code, msgCode, msg = objs.create(name, content)
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    def put(self, project_name, name):
        """Update an object"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', None)
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        status_code, msgCode, msg = objs.update(name, new_name, content)
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    def delete(self, project_name, name):
        """Delete an object"""
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        status_code, msgCode, msg = objs.delete(name)
        return jsonify({'msgCode': msgCode, 'msg': msg}), status_code

    @classmethod
    def init_app(cls, app: Flask, name: str, name_type: str = 'string'):
        view = cls.as_view(f'{name}_api', name)
        app.add_url_rule(f'/projects/<string:project_name>/{name}',
                         defaults={'name': None},
                         view_func=view,
                         methods=['GET'])
        app.add_url_rule(f'/projects/<string:project_name>/{name}',
                         view_func=view,
                         methods=['POST'])
        app.add_url_rule(f'/projects/<string:project_name>/{name}/<{name_type}:name>',
                         view_func=view,
                         methods=['GET', 'PUT', 'DELETE'])
