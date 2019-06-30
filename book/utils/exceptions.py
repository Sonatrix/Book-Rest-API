from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['status'] = response.default_code
        response.data['message'] = response.default_detail

    return response

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
    