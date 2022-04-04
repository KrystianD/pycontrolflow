from abc import ABCMeta, abstractmethod
from typing import Union, Iterable, Any, TypeVar, Optional

from pycontrolflow.IFlowValueProvider import IFlowValueProvider


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...


TComparable = TypeVar('TComparable', bound=Comparable)

TValue = TypeVar("TValue")

TNodeInput = Union[Optional[TValue], IFlowValueProvider[TValue]]
TNodeInputs = Iterable[TNodeInput[TValue]]

__all__ = [
    "TComparable",
    "TNodeInput",
    "TNodeInputs",
]
