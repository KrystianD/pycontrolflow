from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.nodes.logic.LogicOp import LogicOp


class Invert(LogicOp):
    def __init__(self, input_value: IFlowValueProvider[bool]) -> None:
        super().__init__([input_value], lambda values: not values[0])
