import datetime
import logging
from abc import abstractmethod
from typing import Type, Any, TypeVar, Optional, Generic, Union, cast, Sequence, List

import isodate

from pycontrolflow.IFlowValueProvider import IFlowValueProvider, ConstantFlowValueProvider
from pycontrolflow.type_utils import implicit_cast
from pycontrolflow.types import TNodeInput, TNodeInputs

TValue = TypeVar("TValue")

logger = logging.getLogger("controlflow")


class FlowValue(Generic[TValue], IFlowValueProvider[TValue]):
    def __init__(self, name: str, value_type: Type[TValue], default: TValue) -> None:
        self.name = name
        self.type = value_type
        self.default = implicit_cast(default, self.type)
        self._value = self.default

    def set(self, value: Optional[TValue]) -> None:
        if value is None:
            raise ValueError("value cannot be None")

        value = implicit_cast(value, self.type)

        if not self.name.startswith(("_tmp_node.", "_tmp.")):
            logger.debug(f"/{self.name}/ set to /{value}/")
            pass
        self._value = value

    def increment(self, value: TValue) -> None:
        cur_value = self.get_notnull()
        self.set(cur_value + value)  # type: ignore

    def get(self) -> Optional[TValue]:
        return self._value

    def get_notnull(self) -> TValue:
        assert self._value is not None
        return self._value

    # def get_or_default(self, default: TValue) -> TValue:
    #     return default if self._value is None else self._value

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

    def get_type(self) -> Type[TValue]:
        return self.type

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


def wrap_input(input_: TNodeInput[TValue]) -> IFlowValueProvider[TValue]:
    if isinstance(input_, IFlowValueProvider):
        return input_
    else:
        return ConstantFlowValueProvider(input_)


def wrap_input_check_type(input_: TNodeInput[TValue], expected_type: Type[TValue]) -> IFlowValueProvider[TValue]:
    wrapped = wrap_input(input_)
    if wrapped.get_type() != expected_type:
        raise TypeError(f"input type does not match expected type, got: {wrapped.get_type()}, expected: {expected_type}")
    return wrapped


def resolve_value(value: TNodeInput[TValue]) -> Optional[TValue]:
    if isinstance(value, IFlowValueProvider):
        return value.get()
    else:
        return value


def resolve_value_notnull(value: TNodeInput[TValue]) -> TValue:
    if isinstance(value, IFlowValueProvider):
        ret_value = value.get()
    else:
        ret_value = value

    assert ret_value is not None
    return ret_value


def assert_type(value: Any, var_type: Any, allow_null: bool) -> None:
    if not allow_null:
        assert value is not None
    assert isinstance(value, var_type)


def resolve_value_assert(value: TNodeInput[TValue], var_type: Type[TValue], *, allow_null: bool) -> Optional[TValue]:
    if isinstance(value, IFlowValueProvider):
        assert_type(value.get(), var_type, allow_null=allow_null)
        return value.get()
    else:
        assert_type(value, var_type, allow_null=allow_null)
        return value


def resolve_value_assert_not_null(value: TNodeInput[TValue], var_type: Type[TValue]) -> TValue:
    return cast(TValue, resolve_value_assert(value, var_type, allow_null=False))
