from datetime import datetime


def format_datetime(value: datetime) -> str:
    value = value.isoformat()

    if value.endswith("+00:00"):
        value = value[:-6] + "Z"

    return value
