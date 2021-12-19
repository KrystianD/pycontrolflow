from typing import Optional

from pycontrolflow.flow_value import FlowValue
from pycontrolflow.nodes.comparators.PreviousStateCondition import PreviousStateCondition


class EdgeFalling(PreviousStateCondition[bool, bool]):
    def __init__(self, input_name: FlowValue[bool]) -> None:
        super().__init__(input_name)
        input_name.assert_type(bool)

    # noinspection PyMethodMayBeStatic
    def process_values(self, prev_value: Optional[bool], cur_value: Optional[bool]) -> bool:
        prev_is_false = prev_value is False or prev_value is None
        cur_is_false = cur_value is False or cur_value is None
        prev_is_true = not prev_is_false

        return prev_is_true and cur_is_false
