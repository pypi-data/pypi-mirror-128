# Django Rest Structure

This app make your rest api application simple

# Document

## 1. Install by running
`pip install django-rest-structure`
___
## 2. Add middleware to your `MIDDLEWARE` (or `MIDDLEWARE_CLASSES`) setting like this:

```python
MIDDLEWARE = (
   'django_rest_structure.middlewares.middleware.RequestHandlerMiddleware',
   ...
)
```
___
## 3. Add exception handler to your `REST_FRAMEWORK` setting like this:

```python
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'django_rest_structure.results.exception.exception_handler'
    ...
}
```
###### then add to `YOUR-PROJECT/urls.py`
```python
handler404 = 'django_rest_structure.api.views.error_view_404'
handler500 = 'django_rest_structure.api.views.error_view_500'
handler403 = 'django_rest_structure.api.views.error_view_403'
handler400 = 'django_rest_structure.api.views.error_view_400'

```
___


## 4. Create your result messages like:
```python
from django_rest_structure.results.codes import ResultMessageStructure
from django_rest_structure.results.exception import ResultMessages

class MyCustomResultMessages(ResultMessages):
    CUSTOM_ERROR = ResultMessageStructure(1, 'My Custom Error', False, 500)
    # `1` is your result code
    # `My Custom Error` is your result message
    # `False` define result is success or not
    # `500` is http response code
```
___

## 5. Create your custom exception like:
```python
from django_rest_structure.results.exception import Err

class MyCustomError(MyCustomResultMessages, Err):
    def __init__(self, *args, **kwargs):
        super(MyCustomError, self).__init__(*args, **kwargs)

```
___
## 6. Now you should create your views like:

```python
from django_rest_structure.api.views import BaseApiView

class MyView(BaseApiView):
    def post_method(self, request, *args, **kwargs):
        result = {}
        return ResponseStructure(ResultMessages.GET_SUCCESSFULLY, result)
```
#### sample 1:
###### request data: 

```json
{}
```
###### response data: 
```json
{
    "status": {
        "code": 200,
        "message": "Done",
        "is_success": true
    },
    "result": {}
}
```

## 7. Create your serializers like:

### 1. simple serializers 

```python
from django_rest_structure.api.views import BaseApiView
from django_rest_structure.api.serializers import BaseSerializer
from rest_framework import serializers

class MySerializer(BaseSerializer):
    my_field = serializers.CharField()

    def get_response(self):
        # the request available on self.request
        response_data = {
            'my_field': self.validated_data['my_field']
        }
        return ResponseStructure(ResultMessages.GET_SUCCESSFULLY, response_data)



class MyView(BaseApiView):
    def post_method(self, request, *args, **kwargs):
        return MySerializer(request.data, check_is_valid=True, request=request).get_response()


```
#### sample 1:
###### request data: 
```json
{
    "my_field": "test"
}
```
###### response data: 
```json
{
    "status": {
        "code": 200,
        "message": "Done",
        "is_success": true
    },
    "result": {
        "my_field": "test"
    }
}
```
### 2. serializer with custom validation
```python
from django_rest_structure.api.views import BaseApiView
from django_rest_structure.api.serializers import BaseSerializer
from django_rest_structure.api.validations import StrFieldValidation
from rest_framework import serializers

def my_field_vld(value, **extra_params):
    return value.upper()


class MySerializer(BaseSerializer):
    # returned object from StrFieldValidation is available on validated_data
    my_field = serializers.CharField(validators=[StrFieldValidation(
        regex=r'^[A-Za-z]+$',
        error_message='just enter alphabet',
        extra_function=my_field_vld
    )])

    def get_response(self):
        # the request available on self.request
        response_data = {
            'my_field': self.validated_data['my_field']
        }
        return ResponseStructure(ResultMessages.GET_SUCCESSFULLY, response_data)


class MyView(BaseApiView):
    def post_method(self, request, *args, **kwargs):
        return MySerializer(request.data, check_is_valid=True, request=request).get_response()

```
#### sample 1:
###### request data: 
```json
{
    "my_field": "@"
}
```
###### response data: 
```json
{
    "status": {
        "code": 406,
        "message": "Entered Data Is Not Valid",
        "is_success": false
    },
    "result": {
        "my_field": [
            "enter just alphabet"
        ]
    }
}
```
#### sample 2:
###### request data: 
```json
{
    "my_field": "Test"
}
```
###### response data: 
```json
{
    "status": {
        "code": 200,
        "message": "Done",
        "is_success": true
    },
    "result": {
        "my_field": "TEST"
    }
}
```
### 3. list serializer
```python
from django_rest_structure.api.views import BaseApiView
from django_rest_structure.api.serializers import MyListSerializer

class MySerializer(MyListSerializer):

    def get_response(self):
        # the request available on self.request
        my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        response_data = self.paging_structure(
            *self.paging(my_list)
        )
        return ResponseStructure(ResultMessages.GET_SUCCESSFULLY, response_data)


class MyView(BaseApiView):
    def post_method(self, request, *args, **kwargs):
        return MySerializer(request.data, check_is_valid=True, request=request).get_response()

```
#### sample 1:
###### request data: 
```json
{
    "page": 1,
    "count": 5
}
```
###### response data: 
```json
{
    "status": {
        "code": 200,
        "message": "Done",
        "is_success": true
    },
    "result": {
        "list": [
            "a",
            "b",
            "c",
            "d",
            "e"
        ],
        "page": 1,
        "count_in_page": 5,
        "total_count": 12
    }
}
```

## 8. Config your settings

##### change structure response function by adding to your `settings.py`
```python

REST_STRUCTURE_CONF = {
    'response_handler': 'django_rest_structure.results.structure.response_structure'
}

```
###### define your custom function like:
```python

def response_structure(response):
    return {
        'status': {
            'code': response.message.code,
            'message': response.message.message,
            'is_success': response.message.is_success_result,

        },
        'result': response.body
    }

```

##### change logging handler function by adding to your `settings.py`
```python

REST_STRUCTURE_CONF = {
        'log_handler': 'django_rest_structure.logs.console.emmit',
}

```
###### define your custom function like:
```python

import logging
logger = logging.Logger('console')



def emmit(request, response, error, request_time, response_time):
    if error is not None:
        logger.debug(error)


```
## 9. You can see the simple project that use from this package at: [django_rest_structure_sample](https://github.com/ArefMousakhani/django_rest_structure_sample)
