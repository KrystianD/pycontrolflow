from abc import abstractmethod
from typing import TypeVar, Optional

from pycontrolflow.nodes.comparators.PreviousStateCondition import PreviousStateCondition

TValue = TypeVar("TValue")


class Changed(PreviousStateCondition[TValue, bool]):
    @abstractmethod
    def process_values(self, prev_value: Optional[TValue], cur_value: Optional[TValue]) -> bool:
        return prev_value != cur_value
