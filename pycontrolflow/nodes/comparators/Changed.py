from abc import abstractmethod
from typing import TypeVar, Optional, Type, Generic, Any

from pycontrolflow.nodes.comparators.PreviousStateCondition import PreviousStateCondition
from pycontrolflow.types import TNodeInput

TValue = TypeVar("TValue")


class Changed(PreviousStateCondition[TValue, bool], Generic[TValue]):
    def __init__(self, input_: TNodeInput[TValue]) -> None:
        super().__init__(input_)

    def process_values(self, prev_value: TValue, cur_value: TValue) -> bool:
        return prev_value != cur_value
