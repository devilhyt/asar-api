from typing import Union
from flask import Flask, jsonify, current_app, request
import asyncio
import logging
import time
from pydantic import ValidationError


def init_app(app: Flask):
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger.hasHandlers():
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    app.before_request(request_info)
    app.register_error_handler(Exception, handle_exception)

    # test page
    @app.get("/")
    def test_get():
        return "<p>Hello, World!</p>"

    @app.route("/async")
    async def test_async():
        await asyncio.sleep(5)
        return jsonify('async')

    @app.route("/delay")
    def test_block():
        time.sleep(5)
        return jsonify('delay')


def request_info():
    """Debugger for request info"""
    try:
        if request.content_type == 'application/json':
            data = request.json
        elif request.content_type == 'application/x-tar':
            data = 'application/x-tar'
        else:
            data = request.data
        current_app.logger.debug(f'\n  view_args: {request.view_args}\
                                   \n  data     : {data}\
                                   \n  args     : {request.args.to_dict()}')
        # current_app.logger.debug(f'\n  header   : {request.headers}\
        #                            \n  addr     : {request.remote_addr}')
    except:
        pass


def handle_exception(e: Union[Exception, ValidationError]):
    """flask error handler"""
    current_app.logger.error(e)
    # current_app.logger.error(e.args)
    if type(e) == ValidationError:
        arg: dict
        if (len(raw_errors := e.raw_errors) == 1):
            if (args := raw_errors[0].exc.args):
                arg = args[0]
        else:
            arg = {}
        msgCode = arg.get('msgCode', 'validationError')
        msg = arg.get('msg', str(e))
        return jsonify({'msgCode': msgCode, 'msg': msg}), 400
    else:
        return jsonify({'msgCode': 'unexpectedError', 'msg': str(e)}), 400
