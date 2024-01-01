from functools import reduce

from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.nodes.logic.LogicOp import LogicOp


class And(LogicOp):
    def __init__(self, *inputs: IFlowValueProvider[bool]) -> None:
        super().__init__(inputs, lambda values: reduce(lambda a, b: a and b, values, True))
