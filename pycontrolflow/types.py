from typing import Union, Iterable, Any, TypeVar, Optional

from pycontrolflow.IFlowValueProvider import IFlowValueProvider

TValue = TypeVar("TValue")

TNodeInput = Union[Optional[TValue], IFlowValueProvider[TValue]]
TNodeInputs = Iterable[TNodeInput[TValue]]
