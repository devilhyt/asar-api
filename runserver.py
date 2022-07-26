from project import app
from flask import request

if __name__ == '__main__':
    
    @app.get("/")
    def hello_world_get():
        print(request.args.get('mode'))
        return "<p>Hello, World!</p>"

    @app.post("/")
    def hello_world_post():
        print(request.get_json())
        print(request.args.get('mode'))
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)