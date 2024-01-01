from typing import Generic, Type, TypeVar

from pycontrolflow.IFlowValueProvider import IFlowValueProvider

TValue = TypeVar("TValue")


class ReadOnlyFlowValue(Generic[TValue], IFlowValueProvider[TValue]):
    def __init__(self, value_provider: IFlowValueProvider[TValue]):
        self._value_provider = value_provider

    def get(self) -> TValue:
        return self._value_provider.get()

    def get_type(self) -> Type[TValue]:
        return self._value_provider.get_type()
