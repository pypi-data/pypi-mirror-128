import re
from types import FunctionType

from rest_framework import serializers


class ValidationsRegex:
    POSITIVE_INTEGER_REGEX = r'^[0-9]\d*$'
    DATETIME_REGEX = r'^(\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})$'
    DATE_REGEX = r'^(\d{4}\-\d{1,2}\-\d{1,2})$'
    JWT_REGEX = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'
    PASSWORD_REGEX = r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[a-zA-Z]).{8,}$'


class StrFieldValidation:
    DEFAULT_ERROR_MESSAGE = 'Invalid data'

    def __init__(self, regex: str = None, error_message: str = None, extra_function=None,
                 **function_extra_kwargs):
        self.re, self.msg, self.ef = \
            regex, error_message if error_message is not None else self.DEFAULT_ERROR_MESSAGE, extra_function
        self.function_extra_kwargs = function_extra_kwargs

    def __call__(self, value: str):
        self.validated_value = value
        if value is not None and value.strip():
            if self.re is not None and not re.match(self.re, str(value)):
                raise serializers.ValidationError(self.msg)

        if self.ef is not None:
            self.validated_value = self.ef(value, **self.function_extra_kwargs)
