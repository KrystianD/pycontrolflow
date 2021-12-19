from datetime import timedelta, datetime
from typing import Optional


def datetime_isoformat(tdt: datetime, format: Optional[str] = None) -> str: ...


def duration_isoformat(tduration: timedelta, format: Optional[str] = None) -> str: ...


def parse_datetime(datetimestring: str) -> datetime: ...


def parse_duration(datestring: str) -> timedelta: ...
