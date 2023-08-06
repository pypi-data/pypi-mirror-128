from rest_framework.views import APIView
from ..results.codes import ResultMessages
from ..results.exception import Err
from ..results.response import response_handler_dec, ResponseStructure


class BaseApiView(APIView):
    @response_handler_dec
    def get(self, *args, **kwargs):
        return self.get_method(*args, **kwargs)

    def get_method(self, request, *args, **kwargs):
        raise Err(Err.UNDEFINED_METHOD)

    @response_handler_dec
    def post(self, *args, **kwargs):
        return self.post_method(*args, **kwargs)

    def post_method(self, request, *args, **kwargs):
        raise Err(Err.UNDEFINED_METHOD)

    @response_handler_dec
    def put(self, *args, **kwargs):
        return self.put_method(*args, **kwargs)

    def put_method(self, request, *args, **kwargs):
        raise Err(Err.UNDEFINED_METHOD)

    @response_handler_dec
    def delete(self, *args, **kwargs):
        return self.delete_method(*args, **kwargs)

    def delete_method(self, request, *args, **kwargs):
        raise Err(Err.UNDEFINED_METHOD)


@response_handler_dec
def error_view_404(request, *args, **kwargs):
    return ResponseStructure(ResultMessages.PAGE_NOT_FOUND)


@response_handler_dec
def error_view_500(request, *args, **kwargs):
    return ResponseStructure(ResultMessages.UNDEFINED_ERROR)


@response_handler_dec
def error_view_403(request, *args, **kwargs):
    return ResponseStructure(ResultMessages.FORBIDDEN)


@response_handler_dec
def error_view_400(request, *args, **kwargs):
    return ResponseStructure(ResultMessages.BAD_REQUEST)
