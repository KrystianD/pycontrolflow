from abc import abstractmethod
from typing import TypeVar, Generic, Type

TValue = TypeVar("TValue")


class IFlowValueProvider(Generic[TValue]):
    @abstractmethod
    def get(self) -> TValue:
        pass

    @abstractmethod
    def get_type(self) -> Type[TValue]:
        pass


class ConstantFlowValueProvider(IFlowValueProvider[TValue]):
    def __init__(self, value: TValue):
        self._value = value

    def get(self) -> TValue:
        return self._value

    def get_type(self) -> Type[TValue]:
        return type(self._value)
