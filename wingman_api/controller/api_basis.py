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
from ..models.token import Token
from typing import Union

file_types = Union[FileBasis, Intent, Action,
                   Entity, Entity, Slot, Story, Rule, Token]


class ApiBasis(MethodView):
    """Wingman API"""
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
        else:
            r = objs.content
        return jsonify(r), 200

    def post(self, project_name):
        """Create an object"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        objs.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, name):
        """Update an object"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        objs.update(name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, name):
        """Delete an object"""
        # Implement
        prj = Project(project_name)
        objs: file_types = getattr(prj, self.attr_name)
        objs.delete(name)
        return jsonify({"msg": "OK"}), 200

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
