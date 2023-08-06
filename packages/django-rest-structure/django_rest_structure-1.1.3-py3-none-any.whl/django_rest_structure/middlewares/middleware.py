import uuid
from django.utils import timezone
from ..logs.console import emmit
from ..configs import REST_STRUCTURE_CONF


class RequestHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_uid = uuid.uuid4()
        request_time = timezone.now()
        request.body

        response = self.get_response(request)
        REST_STRUCTURE_CONF['log_handler'](request, response, response.err if hasattr(response, 'err') else None,
                                          request_time, timezone.now())
        return response
