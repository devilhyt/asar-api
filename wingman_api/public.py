from flask import Flask, jsonify, current_app, request


def init_app(app: Flask):
    app.before_request(request_info)
    app.register_error_handler(Exception, handle_exception)

    # test page
    @app.get("/")
    def hello_world_get():
        return "<p>Hello, World!</p>"

    @app.post("/<string:test_string>")
    def hello_world_post(test_string):
        return "<p>Hello, World!</p>"

    @app.get("/json")
    def json_test():
        return [{'a': 1}, {'b': 2}]


def request_info():
    """Debugger for request info"""
    try:
        current_app.logger.debug(f'\n  view_args: {request.view_args}\
                                   \n  data     : {request.data}\
                                   \n  args     : {request.args}')
    except:
        pass


def handle_exception(e: Exception):
    """flask error handler"""
    current_app.logger.error(e)
    return jsonify({"Error message": str(e)}), 400
