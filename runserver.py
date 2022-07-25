from project import app
from flask import request

if __name__ == '__main__':
    
    @app.route("/")
    def hello_world():
        print(request.args.get('mode'))
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)