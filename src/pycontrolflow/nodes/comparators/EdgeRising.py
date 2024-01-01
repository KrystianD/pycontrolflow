from typing import Optional

from pycontrolflow.mytypes import TNodeInput
from pycontrolflow.nodes.comparators.PreviousStateCondition import PreviousStateCondition


class EdgeRising(PreviousStateCondition[bool, bool]):
    def __init__(self, input_: TNodeInput[bool]) -> None:
        super().__init__(input_)

    # noinspection PyMethodMayBeStatic
    def process_values(self, prev_value: Optional[bool], cur_value: Optional[bool]) -> bool:
        prev_is_false = prev_value is False
        cur_is_false = cur_value is False
        cur_is_true = not cur_is_false

        return prev_is_false and cur_is_true
