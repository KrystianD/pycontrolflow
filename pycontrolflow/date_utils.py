import datetime
import re
from typing import Optional, Union

_timedelta_map = {
    "ms": datetime.timedelta(milliseconds=1),
    "s": datetime.timedelta(seconds=1),
    "m": datetime.timedelta(minutes=1),
    "h": datetime.timedelta(hours=1),
    "d": datetime.timedelta(days=1),
}


def parse_timedelta(x: Union[str, int, float, datetime.timedelta], default_multiplier: Optional[datetime.timedelta] = None) -> datetime.timedelta:
    if isinstance(x, datetime.timedelta):
        return x

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
    val = datetime.timedelta()
    for part in x.split(" "):
        m = re.match(r"(\d+)(ms|s|m|h|d)", part, re.IGNORECASE)
        if m:
            val += float(m.group(1)) * _timedelta_map[m.group(2)]
        else:
            raise ValueError("invalid spec")

    return val
