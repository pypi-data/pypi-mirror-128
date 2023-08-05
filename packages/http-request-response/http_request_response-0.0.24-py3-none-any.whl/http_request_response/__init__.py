import traceback
from datetime import datetime
from functools import wraps

from flask import current_app as app
from flask import request
from http_status_code.standard import bad_request, request_args_validation_error

from .logging_manager import LoggingManager
from .exception import ApplicationException


class RequestResponse:

    def __init__(self, status_code=None, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def update(self, status_code=200, data=None, message=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)

    def __message_to_str(self, message):
        return message if message is None else str(message)

    def __call__(self, *args, **kwargs):
        return self.__dict__, self.__dict__['status_code']


class RequestUtilities:
    @classmethod
    def try_except(cls, fn):
        """A decorator for all of the actions to do try except"""

        @wraps(fn)
        def wrapper(*args, **kwargs):

            try:
                status, data = fn(*args, **kwargs)

                msg = cls.get_message_header(status)
                LoggingManager.log_info(app, msg)

                if status.code == request_args_validation_error.code:
                    msg += f"\n\nArgs validation response:\n{data}"
                    LoggingManager.log_exception(app, msg)
                else:
                    LoggingManager.log_info(app, msg)


            except ApplicationException as app_exc:
                status = bad_request.deep_copy(str(app_exc))
                data = {}

                msg = cls.prepare_exception_message(status, app_exc)
                LoggingManager.log_exception(app, msg)


            except Exception as exc:
                status = bad_request
                data = {}

                msg = cls.prepare_exception_message(status, exc)
                LoggingManager.log_exception(app, msg)

            rs = RequestResponse(status_code=status.code, message=status.message, data=data)
            return rs()

        return wrapper

    @classmethod
    def prepare_exception_message(cls, status, exc):
        msg = cls.get_message_header(status)
        msg += f"\n\nException: {exc}" \
               f"\nException type: {type(exc)}" \
               f"\n\nFull Traceback:\n{traceback.format_exc()}"

        return msg

    @classmethod
    def pop_fields(cls):
        cls.pop_field('email')
        cls.pop_field('password')
        cls.pop_field('db_uri')

    @staticmethod
    def pop_field(field_name):
        if request.args is not None and field_name in request.args:
            request.args.pop(field_name)

        if request.json is not None and field_name in request.json:
            request.json.pop(field_name)

    @classmethod
    def get_message_header(cls, status):
        cls.pop_fields()

        msg = f"{datetime.utcnow()} UTC." \
              f"\n{app.config.get('APPLICATION_NAME')}" \
              f"\n{app.config.get('ENV_NAME')}." \
              f"\n\nIP: {request.remote_addr}" \
              f"\nURL: {request.url}" \
              f"\nMethod: {request.method}" \
              f"\n\nStatus code: {status.code}" \
              f"\nStatus message: {status.message}" \
              f"\n\nQs args\n{request.args}" \
              f"\n\nBody args:\n{request.json}"

        try:
            # Login endpoint has no claims
            msg += f"\n\nClaims:\n{request.claims}"

        except:
            pass

        return msg
