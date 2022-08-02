from wingman_api import app

if __name__ == '__main__':
    
    # test page
    @app.get("/")
    def hello_world_get():
        return "<p>Hello, World!</p>"
    
    from flask import request
    @app.post("/<string:test_string>")
    def hello_world_post(test_string):
        print(request.view_args)
        print(request.json)
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)