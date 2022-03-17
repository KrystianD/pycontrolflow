from datetime import datetime, timedelta
from typing import Any, TypeVar, List, Callable

from pycontrolflow.flow_value import resolve_value
from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode
from pycontrolflow.types import TNodeInputs

TOutput = TypeVar("TOutput")


class Transform(FlowSingleOutputNode[TOutput]):
    def __init__(self, transformer_cb: Callable[[List[Any]], TOutput], *input_values: TNodeInputs[Any]) -> None:
        super().__init__(input_values)
        self.input_values = input_values
        self.transformer_cb = transformer_cb

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)

        output = self.transformer_cb([resolve_value(x) for x in self.input_values])

        self.set_output(output)
