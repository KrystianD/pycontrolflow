import datetime
from abc import abstractmethod
from typing import Type, Any, TypeVar, Optional, Generic, Union, cast

import isodate

from pycontrolflow.IFlowValueProvider import IFlowValueProvider

TValue = TypeVar("TValue")


class FlowValue(Generic[TValue], IFlowValueProvider):
    def __init__(self, name: str, value_type: Type[TValue], default: Optional[TValue]) -> None:
        self.name = name
        self.type = value_type
        self.default = default
        self._value = default

    def set(self, value: Optional[TValue]) -> None:
        assert value is None or type(value) == self.type, f"{type(value)} not equal to {self.type}"

        if not self.name.startswith(("_tmp_node.", "_tmp.")):
            print(f"{self.name} set to {value}")
        self._value = value

    def increment(self, value: TValue) -> None:
        cur_value = self.get()
        assert cur_value is not None
        self.set(cur_value + value)  # type: ignore

    def get(self) -> Optional[TValue]:
        return self._value

    def get_notnull(self) -> TValue:
        assert self._value is not None
        return self._value

    def get_or_default(self, default: TValue) -> TValue:
        return default if self._value is None else self._value

    def isnull(self) -> bool:
        return self._value is None

    def isnotnull(self) -> bool:
        return self._value is not None

    def assert_type(self, type_to_check: Type[TValue]) -> None:
        assert self.type == type_to_check

    def to_json(self) -> Optional[Union[str, float]]:
        if self._value is None:
            return None
        elif self.type == datetime.datetime:
            return isodate.datetime_isoformat(cast(datetime.datetime, self._value))
        elif self.type == datetime.timedelta:
            return isodate.duration_isoformat(cast(datetime.timedelta, self._value))
        else:
            return cast(Union[str, float], self._value)

    def from_json(self, data: Optional[Union[str, float]]) -> None:
        if data is None:
            self._value = None
        elif self.type == datetime.datetime:
            self._value = cast(TValue, isodate.parse_datetime(cast(str, data)))
        elif self.type == datetime.timedelta:
            self._value = cast(TValue, isodate.parse_duration(cast(str, data)))
        else:
            self._value = cast(TValue, data)

    @abstractmethod
    def start_cycle(self) -> None:
        pass


class FlowVariable(FlowValue[TValue]):
    def start_cycle(self) -> None:
        self._value = self.default


class FlowMemoryCell(FlowValue[TValue]):
    def __init__(self, name: str, value_type: Type[TValue], default: Any, persistent: bool) -> None:
        super().__init__(name, value_type, default)
        self.persistent = persistent

    def start_cycle(self) -> None:
        pass
