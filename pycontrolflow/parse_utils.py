import re
from datetime import time, datetime, timedelta
from typing import Union, Optional


def parse_time(time_val: Union[time, str]) -> time:
    if isinstance(time_val, time):
        return time_val
    elif isinstance(time_val, str):
        if re.match("\d+:\d+:\d+", time_val) is not None:
            return datetime.strptime(time_val, "%H:%M:%S").time()
        elif re.match("\d+:\d+", time_val) is not None:
            return datetime.strptime(time_val, "%H:%M").time()
        else:
            raise ValueError
    else:
        raise ValueError


_timedelta_map = {
    "ms": timedelta(milliseconds=1),
    "s": timedelta(seconds=1),
    "m": timedelta(minutes=1),
    "h": timedelta(hours=1),
    "d": timedelta(days=1),
}


def parse_timedelta(x: Union[str, int, float], default_multiplier: Optional[timedelta] = None) -> timedelta:
    # parse numbers
    if isinstance(x, (int, float)):
        if default_multiplier is None:
            raise ValueError("raw number not allowed")
        else:
            return x * default_multiplier

    # parse number passed as string
    if default_multiplier is not None:
        try:
            return float(x) * default_multiplier
        except ValueError:
            pass

    # parse parts
    val = timedelta()
    for part in x.split(" "):
        m = re.match(r"(\d+)(ms|s|m|h|d)", part, re.IGNORECASE)
        if m:
            val += float(m.group(1)) * _timedelta_map[m.group(2)]
        else:
            raise ValueError("invalid spec")

    return val
