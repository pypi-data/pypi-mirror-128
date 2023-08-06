import json
import typing

from ..core.field import BaseField


class DictField(BaseField):

    def serialize(self, value: typing.Optional[typing.Dict]) -> typing.Optional[typing.Dict]:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Optional[typing.Dict]:
        if value is None:
            return None

        if isinstance(value, dict):
            return value

        if isinstance(value, list):
            return {}

        if isinstance(value, str):
            return from_json(value)


def from_json(value: str) -> typing.Dict[str, typing.Any]:
    if not value:
        return {}

    try:
        json_value = json.loads(value)
    except ValueError:
        raise ValueError(f'<{value}> is not dict')

    if not isinstance(json_value, dict):
        raise ValueError(f'<{value}> is not dict')

    return json_value
