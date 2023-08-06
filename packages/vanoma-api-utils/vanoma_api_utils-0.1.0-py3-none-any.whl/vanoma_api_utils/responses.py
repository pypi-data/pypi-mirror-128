from rest_framework.response import Response


def generic_error(status, error_code, error_message, headers={}):
    data = {"error_code": error_code, "error_message": error_message}
    return Response(status=status, data=data, headers=headers)
