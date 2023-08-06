import traceback

from django.template import Template, Context
from rest_framework.exceptions import ParseError, AuthenticationFailed, NotAuthenticated

from .codes import ResultMessages
from .codes import ResultMessageStructure
from .response import ResponseStructure, Request


class Err(ResultMessages, Exception):
    def __init__(self, result_message: ResultMessageStructure, more_data=None, **message_context):
        self.more_data = more_data
        self.message = Template(result_message.message).render(Context(message_context))
        self.code = result_message.code
        self.http_code = result_message.http_code
        super().__init__(self.message)


def exception_handler(exc, context):
    exception_type = type(exc)
    additional_data = None
    err = None
    if exception_type is ParseError:
        result_message = Err.INVALID_CONTENT_TYPE

    elif exception_type in [AuthenticationFailed, NotAuthenticated]:
        result_message = Err.AUTHENTICATION_FAIL

    else:
        if hasattr(exc, 'code'):
            exc: Err
            result_message, additional_data = ResultMessageStructure(exc.code, exc.message, False, exc.http_code), exc.more_data
        else:
            err = traceback.format_exc()
            result_message = Err.UNDEFINED_ERROR

    return Request.generate_response_data(ResponseStructure(result_message, additional_data, err))
