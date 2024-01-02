from typing import Generic, Callable, Type, TypeVar

from pycontrolflow.IFlowValueProvider import IFlowValueProvider

TValue = TypeVar("TValue")


class ComputedReadOnlyFlowValue(Generic[TValue], IFlowValueProvider[TValue]):
    def __init__(self, value_provider: IFlowValueProvider[TValue], converter: Callable[[TValue], TValue]):
        self._value_provider = value_provider
        self._converter = converter

    def get(self) -> TValue:
        return self._converter(self._value_provider.get())

    def get_type(self) -> Type[TValue]:
        return self._value_provider.get_type()
