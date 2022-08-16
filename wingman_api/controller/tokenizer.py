from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from wingman_api.models.project import Project
import jieba


class TokenizerAPI(MethodView):
    """Wingman Tokenizer API"""
    decorators = [jwt_required()]

    def post(self, project_name):
        """tokenize"""
        # Receive
        sentence = request.json.get('sentence')
        # Implement
        prj = Project(project_name)
        prj.tokens.gen_jieba_dict()

        tokenizer = jieba.Tokenizer()
        tokenizer.load_userdict(str(prj.tokens.jieba_dict))
        tokenized = tokenizer.tokenize(sentence)

        tokens = [{'token': token, 'start': start, 'end': end}
                  for (token, start, end) in tokenized]
        return jsonify(tokens), 200


def init_app(app: Flask):
    tokenizer_view = TokenizerAPI.as_view('tokenizer_api')
    app.add_url_rule('/projects/<string:project_name>/tokenizer',
                     view_func=tokenizer_view,
                     methods=['POST'])
