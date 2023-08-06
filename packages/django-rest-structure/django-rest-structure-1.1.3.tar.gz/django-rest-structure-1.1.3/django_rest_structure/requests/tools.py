import hashlib

from django.core.handlers.wsgi import WSGIRequest


def get_client_ip(request: WSGIRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_agent(request: WSGIRequest) -> str:
    return request.headers.get('User-Agent')


def get_client_fingerprint(request: WSGIRequest):
    fingerprint_raw = "".join(
        (request.META.get("HTTP_USER_AGENT", ""),
         request.META.get("HTTP_ACCEPT_ENCODING", ""))
    )
    return hashlib.md5(
        fingerprint_raw.encode('utf-8')).hexdigest()
