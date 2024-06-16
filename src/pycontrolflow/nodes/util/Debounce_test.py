import unittest
from datetime import datetime, timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.util.Debounce import Debounce


def dt(x: int) -> datetime:
    return datetime(2020, 1, 1, 15, 0, x)


class DebounceTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        test1 = executor.memory("test1", bool, initial_value=False)
        test_met = executor.var("test_met", bool)

        executor.add([
            Debounce[bool](test1, debounce_time=timedelta(seconds=10)).to(test_met),
        ])

        test1.set(True)
        executor.run(dt(0))
        self.assertTrue(test_met.get())

        test1.set(False)
        executor.run(dt(2))
        self.assertTrue(test_met.get())

        test1.set(False)
        executor.run(dt(12))
        self.assertFalse(test_met.get())

        test1.set(False)
        executor.run(dt(25))
        self.assertFalse(test_met.get())

        test1.set(True)
        executor.run(dt(26))
        self.assertTrue(test_met.get())
