import uuid
from django.db import models


class PrimaryKeyField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs["editable"] = False
        kwargs["primary_key"] = True
        kwargs["default"] = uuid.uuid4
        super().__init__(*args, **kwargs)


class StringField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 150
        super().__init__(*args, **kwargs)
