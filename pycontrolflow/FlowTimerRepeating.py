from datetime import timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.FlowTimer import FlowTimer
from pycontrolflow.flow_value import FlowVariable


class FlowTimerRepeating(FlowTimer):
    def __init__(self, flow_executor: FlowExecutor, name: str, interval: timedelta) -> None:
        super().__init__(name)
        self.interval = interval

        self._timer = timedelta()
        self.elapsed = FlowVariable(flow_executor, name + ".elapsed", bool, False)

    def start_cycle(self) -> None:
        self.elapsed.set(False)

    def process(self, delta: timedelta) -> None:
        self._timer += delta

        if self._timer > self.interval:
            self.elapsed.set(True)
            self._timer = timedelta()

    def process_after(self) -> None:
        pass
