import datetime
import typing

from ..core import BaseField

HOUR_MINUTE_FORMAT = '%H:%M'
HOUR_MINUTE_SECOND_FORMAT = '%H:%M:%S'

DATE_FORMAT = '%d.%m.%Y'
ISO_DATE_FORMAT = '%Y-%m-%d'

ISO_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ISO_DATETIME_FORMAT_WITH_T = '%Y-%m-%dT%H:%M:%S'
DATE_FORMATS = [DATE_FORMAT, ISO_DATE_FORMAT]
DATETIME_FORMATS = [ISO_DATETIME_FORMAT, ISO_DATETIME_FORMAT_WITH_T]
TIME_FORMATS = [HOUR_MINUTE_FORMAT, HOUR_MINUTE_SECOND_FORMAT]


class DateField(BaseField):
    def serialize(self, value: datetime.date) -> typing.Any:
        return value.isoformat()

    def deserialzie(self, value: typing.Any) -> typing.Optional[datetime.date]:
        if not value:
            return None
        if isinstance(value, str):
            return parse_date(value, DATE_FORMATS).date()
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value


class DateTimeField(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value.isoformat()

    def deserialzie(self, value: typing.Any) -> typing.Optional[datetime.datetime]:
        if value is None:
            return None
        if isinstance(value, str):
            return parse_date(value, DATETIME_FORMATS)
        if isinstance(value, datetime.datetime):
            return value


class TimeField(BaseField):
    def serialize(self, value: datetime.time) -> str:
        return value.isoformat()

    def deserialzie(self, value: typing.Any) -> typing.Optional[datetime.time]:
        if value is None:
            return None

        if isinstance(value, str):
            parsed_datetime = parse_date(value, [*TIME_FORMATS, *DATETIME_FORMATS])
            return parsed_datetime.time()
        if isinstance(value, datetime.time):
            return value
        if isinstance(value, datetime.datetime):
            return value.time()


def parse_date(date_string: str, formats: typing.List[str]) -> datetime.datetime:
    for format_ in formats:
        try:
            date = datetime.datetime.strptime(date_string, format_)
            return date
        except:  # noqa
            pass
    raise ValueError(f'{date_string} is not date')
