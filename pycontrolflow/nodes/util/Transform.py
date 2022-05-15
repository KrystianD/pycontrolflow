from datetime import datetime, timedelta
from typing import Any, TypeVar, List, Callable, Generic

from pycontrolflow.flow_value import wrap_input
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInput

TOutput = TypeVar("TOutput")

TInputParams = TNodeInput[Any]


class Transform(FlowSingleOutputNode[TOutput], Generic[TOutput]):
    def __init__(self, transformer_cb: Callable[[List[TInputParams]], TOutput], *input_values: TInputParams) -> None:
        self.input_values = [wrap_input(x) for x in input_values]

        super().__init__(self.input_values)

        self.transformer_cb = transformer_cb

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        output = self.transformer_cb([x.get_notnull() for x in self.input_values])

        self.set_output(output)
