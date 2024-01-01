from typing import List, TYPE_CHECKING, Iterable

from pycontrolflow.nodes.FlowNode import FlowNode

if TYPE_CHECKING:
    from pycontrolflow.FlowExecutor import FlowExecutor


class Flow:
    def __init__(self) -> None:
        self.items: List[FlowNode] = []

    def append(self, items: Iterable[FlowNode]) -> None:
        self.items += items

    def set_executor(self, flow_executor: 'FlowExecutor') -> None:
        for item in self.items:
            item.set_executor(flow_executor)
            for subflow in item.subflows:
                subflow.set_executor(flow_executor)

    def setup(self) -> None:
        for item in self.items:
            item.setup()
            for subflow in item.subflows:
                subflow.setup()

    @staticmethod
    def create(*items: FlowNode) -> 'Flow':
        flow = Flow()
        flow.append(items)
        return flow
