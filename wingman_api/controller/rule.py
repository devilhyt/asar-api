from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class RuleAPI(MethodView):
    """Wingman Rule API"""
    decorators = [jwt_required()]

    def get(self, project_name, rule_name):
        """Get rules
        :param rule_name:
            If rule_name is None, then return all rules.\n
            Else, then return a rule object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if rule_name:
            obj = prj.rules.get(rule_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.rules.names
            return jsonify(names), 200
        else:
            content = prj.rules.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create a rule"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.rules.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, rule_name):
        """Update a rule"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.rules.update(rule_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, rule_name):
        """Delete a rule"""
        # Implement
        prj = Project(project_name)
        prj.rules.delete(rule_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):
    rule_view = RuleAPI.as_view('rule_api')
    app.add_url_rule('/projects/<string:project_name>/rules',
                     defaults={'rule_name': None},
                     view_func=rule_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/rules',
                     view_func=rule_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/rules/<string:rule_name>',
                     view_func=rule_view,
                     methods=['GET', 'PUT', 'DELETE'])
