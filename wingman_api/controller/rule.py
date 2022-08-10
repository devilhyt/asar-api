from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class RuleAPI(MethodView):
    """Wingman Rule API"""

    @jwt_required()
    def get(self, project_name, rule_name):
        """
        :param rule_name:
            If rule_name is None, then get the names of all rules.\n
            If rule_name is not None, then get a rule object.
        """

        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if rule_name:
            rule_obj = prj.rule.content[rule_name]
            return jsonify(rule_obj), 200
        elif mode == 'name':
            rule_names = prj.rule.names
            return jsonify({'rule_names': rule_names}), 200
        else:
            rules = prj.rule.content
            return jsonify(rules), 200

    @jwt_required()
    def post(self, project_name):
        """Create a rule"""

        # Receive
        rule_name = request.json.get('rule_name')
        # Implement
        prj = Project(project_name)
        prj.rule.create(rule_name)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def put(self, project_name, rule_name):
        """Update a rule"""

        # Receive
        content = request.json
        new_rule_name = content.pop('new_rule_name', None)
        # Implement
        prj = Project(project_name)
        prj.rule.update(rule_name, new_rule_name, content)
        return jsonify({"msg": "OK"}), 200

    @jwt_required()
    def delete(self, project_name, rule_name):
        """Delete a rule"""

        # Implement
        prj = Project(project_name)
        prj.rule.delete(rule_name)
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
