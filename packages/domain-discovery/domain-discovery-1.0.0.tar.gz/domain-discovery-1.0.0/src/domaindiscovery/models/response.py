import copy
import datetime
import re

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing

_re_date_format = re.compile(r'^\d\d\d\d-\d\d-\d\d$')
_re_datetime_format = re.compile(
    r'^(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d)\+(\d\d):(\d\d)$')


def _datetime_value(values: dict, key: str) -> datetime.datetime or None:
    if key in values and values[key] is not None:
        value = values[key]
        match = _re_datetime_format.fullmatch(value)
        if match is not None:
            (dt, tz_hours, tz_minutes) = match.groups()
            value = "{}+{}{}".format(dt, tz_hours, tz_minutes)
            return datetime.datetime.strptime(
                value, '%Y-%m-%dT%H:%M:%S%z')

    return None


def _date_value(values: dict, key: str) -> datetime.date or None:
    if key in values and values[key] is not None:
        if _re_date_format.match(values[key]) is not None:
            return datetime.datetime.strptime(
                values[key], '%Y-%m-%d').date()

    return None


def _string_value(values: dict, key: str) -> str:
    if key in values and values[key]:
        return str(values[key])
    return ''


def _int_value(values: dict, key: str) -> int:
    if key in values and values[key]:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _timestamp2datetime(timestamp: int) -> datetime.datetime or None:
    if timestamp is not None:
        return datetime.datetime.fromtimestamp(timestamp)
    return None


class Response(BaseModel):
    domains_count: int
    if sys.version_info < (3, 9):
        domains_list: typing.List[str]
    else:
        domains_list: [str]

    def __init__(self, values):
        super().__init__()

        self.domains_count = 0
        self.domains_list = []

        if values is not None:
            self.domains_count = _int_value(values, 'domainsCount')
            self.domains_list = _list_value(values, 'domainsList')


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.int = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
