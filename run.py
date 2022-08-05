from wingman_api.main import app

if __name__ == '__main__':
    
    # test page
    @app.get("/")
    def hello_world_get():
        return "<p>Hello, World!</p>"

    from flask import request

    @app.post("/<string:test_string>")
    def hello_world_post(test_string):
        app.logger.info(request.view_args)
        app.logger.info(request.json)
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)
