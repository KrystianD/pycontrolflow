from datetime import datetime, timedelta
from typing import List, Optional, Union

from pycontrolflow.Flow import Flow
from pycontrolflow.IFlowValueProvider import IFlowValueProvider
from pycontrolflow.nodes.FlowNode import FlowNode


class If(FlowNode):
    def __init__(self, condition: IFlowValueProvider[bool], if_flow: Union[Flow, List[FlowNode]],
                 else_flow: Optional[Union[Flow, List[FlowNode]]] = None) -> None:
        super().__init__([condition])
        self.condition = condition
        self.if_flow = if_flow if isinstance(if_flow, Flow) else Flow.create(*if_flow)
        if else_flow is None:
            self.else_flow = None
        else:
            self.else_flow = else_flow if isinstance(else_flow, Flow) else Flow.create(*else_flow)

        self.register_subflow(self.if_flow)
        self.register_subflow(self.else_flow)

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        super().process(cur_date, delta)
        value = self.condition.get()
        if value:
            for line in self.if_flow.items:
                line.process(cur_date, delta)
        else:
            if self.else_flow is not None:
                for line in self.else_flow.items:
                    line.process(cur_date, delta)
