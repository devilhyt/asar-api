from flask import Flask, jsonify, current_app


def init_app(app: Flask):
    app.register_error_handler(Exception, handle_exception)

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


def handle_exception(e: Exception):
    """flask error handler"""
    current_app.logger.error(e)
    return jsonify({"msg": str(e)}), 400
