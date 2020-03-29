from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler


class ServerException(APIException):
    def __init__(self, message, errors=None):
        super().__init__(errors)
        self.message = message


def server_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        if isinstance(exc, ServerException) and exc.message:
            response.data['message'] = exc.message
        elif isinstance(response.data, ReturnDict):
            if 'error_text' in response.data:
                response.data['message'] = response.data['error_text'][0]
            else:
                message = [f'{key} - {value[0]}' for key, value in response.data.items() if key != 'status_code']
                response.data['message'] = ' & '.join(message)
        elif isinstance(response.data, dict) and 'detail' in response.data:
            response.data['message'] = response.data['detail']

    return response
