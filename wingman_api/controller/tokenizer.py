from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project
import jieba

class TokenizerAPI(MethodView):
    """Wingman Tokenizer API"""

    @jwt_required()
    def post(self, project_name):
        """tokenize"""
        
        # Receive
        sentence = request.json.get('sentence')
        # Implement
        tokenized = jieba.tokenize(sentence)
        tokens = [{'word': word, 'start': start, 'end': end} for (word, start, end) in tokenized]
        return jsonify({"tokens": tokens}), 200

    @jwt_required()
    def put(self, project_name):
        """Update tokens"""
        
        # Receive
        content = request.json
        # tokens = content.pop('tokens', None)
        # # Implement
        # prj = Project(project_name)
        # prj.token.update('tokens', None, tokens)
        return jsonify({"msg": "OK"}), 200


def init_app(app: Flask):

    intent_view = TokenizerAPI.as_view('tokenizer_api')
    app.add_url_rule('/projects/<string:project_name>/tokenizer',
                     view_func=intent_view,
                     methods=['POST', 'PUT'])
