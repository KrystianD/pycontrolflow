from abc import abstractmethod
from typing import Any, TypeVar, Generic

TValue = TypeVar("TValue")


class IFlowValueProvider(Generic[TValue]):
    @abstractmethod
    def get(self) -> Any:
        pass
