from abc import abstractmethod
from typing import Any, TypeVar, Generic, Optional, Type

TValue = TypeVar("TValue")


class IFlowValueProvider(Generic[TValue]):
    @abstractmethod
    def get(self) -> Optional[TValue]:
        pass

    @abstractmethod
    def get_type(self) -> Type[TValue]:
        pass

    def get_notnull(self) -> TValue:
        value = self.get()
        assert value is not None
        return value


class ConstantFlowValueProvider(IFlowValueProvider[TValue]):
    def __init__(self, value: TValue):
        self._value = value

    def get(self) -> Optional[TValue]:
        return self._value

    def get_type(self) -> Type[TValue]:
        return type(self._value)
