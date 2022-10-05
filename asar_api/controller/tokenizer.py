from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
# from ..models.project import Project
# import jieba
from ckip_transformers.nlp import CkipWordSegmenter
from ..config import ALBERT_BASE_CHINESE_WS_DIR
from ..utils.utils import convert_words_to_tokens

class TokenizerAPI(MethodView):
    """Asar Tokenizer API"""
    decorators = [jwt_required()]
    init_every_request = False
    
    def __init__(self) -> None:
        self.ws_driver = CkipWordSegmenter(model_name=ALBERT_BASE_CHINESE_WS_DIR)

    def post(self, project_name):
        """tokenize"""
        # Receive
        sentence = request.json.get('sentence')
        # Implement
        # prj = Project(project_name)
        # prj.tokens.gen_jieba_dict()

        # tokenizer = jieba.Tokenizer()
        # tokenizer.load_userdict(str(prj.tokens.jieba_dict_file))
        # tokenized = tokenizer.tokenize(sentence)

        # tokens = [{'token': token, 'start': start, 'end': end}
        #           for (token, start, end) in tokenized]
        if sentence:
            ws = self.ws_driver([sentence])
            tokens = convert_words_to_tokens(ws[0], sentence)
        else:
            tokens = []
        return jsonify(tokens), 200

    @classmethod
    def init_app(cls, app: Flask):
        tokenizer_view = cls.as_view('tokenizer_api')
        app.add_url_rule('/projects/<string:project_name>/tokenizer',
                        view_func=tokenizer_view,
                        methods=['POST'])
