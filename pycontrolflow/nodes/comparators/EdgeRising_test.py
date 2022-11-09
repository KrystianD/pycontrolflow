import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.EdgeRising import EdgeRising


class EdgeRisingTest(unittest.TestCase):
    def test(self) -> None:
        executor = FlowExecutor()

        in1 = executor.memory("test1", bool, initial_value=False)
        out = executor.var("out", bool)

        executor.add([
            EdgeRising(in1).to(out),
        ])

        in1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertFalse(out.get())

        in1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 1, 00))
        self.assertTrue(out.get())

        in1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 1, 00))
        self.assertFalse(out.get())
