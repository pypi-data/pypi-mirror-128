import logging
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions, status
from rest_framework.views import set_rollback
from .responses import generic_error
from .constants import ERROR_CODE


def exception_handler(exc, context):
    """
    Mostly copied from https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py#L71
    """
    if isinstance(exc, Http404):
        return generic_error(
            status.HTTP_404_NOT_FOUND,
            ERROR_CODE.RESOURCE_NOT_FOUND,
            str(exc),
        )

    if isinstance(exc, PermissionDenied):
        return generic_error(
            status.HTTP_403_FORBIDDEN,
            ERROR_CODE.RESOURCE_NOT_FOUND,
            str(exc),
        )

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, list):
            message = ". ".join(exc.detail)
        elif isinstance(exc.detail, dict):
            errors = ["{}-{}".format(k, e) for k, e in exc.detail.items()]
            message = ". ".join(errors)
        else:
            message = exc.detail

        set_rollback()
        return generic_error(
            status.HTTP_400_BAD_REQUEST,
            ERROR_CODE.INVALID_REQUEST,
            message,
            headers,
        )

    # TODO: use sentry to report 500
    logging.error(str(exc), exc_info=True)

    return generic_error(
        status.HTTP_500_INTERNAL_SERVER_ERROR, ERROR_CODE.INTERNAL_ERROR, str(exc)
    )
