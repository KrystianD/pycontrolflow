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
