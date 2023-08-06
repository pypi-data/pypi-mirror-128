import logging

logger = logging.Logger('console')


def emmit(request, response, error, request_time, response_time):
    if error is not None:
        print(error)
        # logger.debug(error)
