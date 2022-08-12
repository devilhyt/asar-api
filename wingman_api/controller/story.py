from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project


class StoryAPI(MethodView):
    """Wingman Story API"""
    decorators = [jwt_required()]

    def get(self, project_name, story_name):
        """Get stories
        :param story_name:
            If story_name is None, then return all stories.\n
            Else, then return a story object.
        """
        # Receive
        mode = request.args.get('mode')
        # Implement
        prj = Project(project_name)
        if story_name:
            obj = prj.stories.get(story_name)
            return jsonify(obj), 200
        elif mode == 'name':
            names = prj.stories.names
            return jsonify(names), 200
        else:
            content = prj.stories.content
            return jsonify(content), 200

    def post(self, project_name):
        """Create a story"""
        # Receive
        name = request.json.get('name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.stories.create(name, content)
        return jsonify({"msg": "OK"}), 200

    def put(self, project_name, story_name):
        """Update a story"""
        # Receive
        new_name = request.json.get('new_name')
        content = request.json.get('content', {})
        # Implement
        prj = Project(project_name)
        prj.stories.update(story_name, new_name, content)
        return jsonify({"msg": "OK"}), 200

    def delete(self, project_name, story_name):
        """Delete a story"""
        # Implement
        prj = Project(project_name)
        prj.stories.delete(story_name)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):
    story_view = StoryAPI.as_view('story_api')
    app.add_url_rule('/projects/<string:project_name>/stories',
                     defaults={'story_name': None},
                     view_func=story_view,
                     methods=['GET'])
    app.add_url_rule('/projects/<string:project_name>/stories',
                     view_func=story_view,
                     methods=['POST'])
    app.add_url_rule('/projects/<string:project_name>/stories/<string:story_name>',
                     view_func=story_view,
                     methods=['GET', 'PUT', 'DELETE'])
