from rest_framework.response import Response
from rest_framework import status

def custom_response(status_bool, message, data=None, http_status=status.HTTP_200_OK):
    """
    A standardized response format for APIs.

    Args:
        status_bool (bool): True or False indicating the success of the operation.
        message (str): Message explaining the result of the operation.
        data (dict, optional): Any additional data to return with the response.
        http_status (int, optional): HTTP status code (default is 200 OK).

    Returns:
        Response: A DRF Response object with a consistent structure.
    """
    if data:
        response = {
            "status": status_bool,
            "message": message,
            "data": data
        }
    else:
        response = {
            "status": status_bool,
            "message": message
        }
    
    return Response(response, status=http_status)