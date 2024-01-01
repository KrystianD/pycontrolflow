from abc import abstractmethod
from typing import Union, Iterable, TypeVar, Protocol

from pycontrolflow.IFlowValueProvider import IFlowValueProvider


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: 'TComparable', other: 'TComparable') -> bool: ...


TComparable = TypeVar('TComparable', bound=Comparable)

TValue = TypeVar("TValue")

TNodeInput = Union[IFlowValueProvider[TValue], TValue]
TNodeInputs = Iterable[TNodeInput[TValue]]

__all__ = [
    "TComparable",
    "TNodeInput",
    "TNodeInputs",
]
