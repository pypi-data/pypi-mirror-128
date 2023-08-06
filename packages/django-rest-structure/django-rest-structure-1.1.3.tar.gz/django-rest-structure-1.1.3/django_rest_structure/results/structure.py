def response_structure(response):
    return {
        'status': {
            'code': response.message.code,
            'message': response.message.message,
            'is_success': response.message.is_success_result,

        },
        'result': response.body
    }
