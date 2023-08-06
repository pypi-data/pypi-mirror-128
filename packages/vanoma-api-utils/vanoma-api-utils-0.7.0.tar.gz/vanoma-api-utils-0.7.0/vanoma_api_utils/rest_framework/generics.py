from typing import Any, Type
from rest_framework import generics
from rest_framework.serializers import Serializer
from .exceptions import InvalidAPIVersion


class GenericAPIView(generics.GenericAPIView):
    """
    Extends GenericAPIView to add support for resolving serializer class based on the requested API version.
    """

    def get_serializer_class(self, *args: Any, **kwargs: Any) -> Type[Serializer]:
        handler_name = "get_v{}_serializer_class".format(self.request.version)
        handler = getattr(self, handler_name, self.invalid_api_version)
        return handler()

    def invalid_api_version(self) -> None:
        raise InvalidAPIVersion()
