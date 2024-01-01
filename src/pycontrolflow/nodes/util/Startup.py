from datetime import datetime, timedelta

from pycontrolflow.nodes.FlowSingleOutputNode import FlowSingleOutputNode


class Startup(FlowSingleOutputNode[bool]):
    def __init__(self) -> None:
        super().__init__([])

        self.first_run = True

    def process(self, cur_date: datetime, delta: timedelta) -> None:
        prev = self.first_run
        self.first_run = False

        self.set_output(prev)
