import traceback
from datetime import datetime
from functools import wraps
from flask import (
    Flask,
    jsonify,
    Response
)

class ResponseFormatter():
    def __init__(self):
        self.response_code = 200
        self.error_code = 101
        self.error_message = "Unhandled rejection. Please try after some time or contact admin"
        self.formatted_result = {
            "code": self.response_code,
            "status": "success",
            "error": False,
            "error_code": None,
            "reason": "",
            "data": None
        }

    def set_response_code(self, code):
        self.response_code = code

    def set_error_code(self, code):
        self.error_code = code

    def set_error_message(self, message):
        self.error_message = message

    def success_response(self, data=None, pagination=None):
        if data:
            self.formatted_result["data"] = dict()
            self.formatted_result["data"]["result"] = data
            if pagination:
                self.formatted_result["data"]["pagination"] = pagination

        return jsonify(self.formatted_result), self.response_code

    def error_response(self):
        self.formatted_result["code"] = self.response_code
        self.formatted_result["status"] = "failure"
        self.formatted_result["error"] = True
        self.formatted_result["error_code"] = self.error_code
        self.formatted_result["reason"] = self.error_message

        return jsonify(self.formatted_result), self.response_code



def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = ResponseFormatter()
        try:
            if isinstance(f(*args, **kwargs), tuple):
                retval, pagination = f(*args, **kwargs)
                return res.success_response(retval, pagination)
            else:
                retval = f(*args, **kwargs)
                return res.success_response(retval)
        except Exception as e:
            traceback.print_exc()
            res.set_response_code(500)
            if (len(e.args) > 1):
                res.set_error_code(e.args[0])
                res.set_error_message(e.args[1])
                if (len(e.args) > 2):
                    res.set_response_code(e.args[2])
            elif (len(e.args) == 1):
                # res.set_error_message(e.message)
                res.set_error_message("There is some error")
            else:
                print(traceback.format_exc())
            return res.error_response()
    return decorated_function
