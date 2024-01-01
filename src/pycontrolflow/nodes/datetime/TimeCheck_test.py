import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.datetime.TimeCheck import TimeCheck


class TimeCheckTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var1 = executor.var("var1", bool)

        executor.add([
            TimeCheck("14:00", "16:00").to(var1),
        ])

        executor.run(datetime(2020, 1, 1, 15, 00))
        self.assertTrue(var1.get())

        executor.run(datetime(2020, 1, 1, 17, 00))
        self.assertFalse(var1.get())

    def test1_cross(self) -> None:
        executor = FlowExecutor()

        var1 = executor.var("var1", bool)

        executor.add([
            TimeCheck("20:00", "04:00").to(var1),
        ])

        executor.run(datetime(2020, 1, 1, 15, 00))
        self.assertFalse(var1.get())

        executor.run(datetime(2020, 1, 1, 22, 00))
        self.assertTrue(var1.get())

        executor.run(datetime(2020, 1, 1, 2, 00))
        self.assertTrue(var1.get())

        executor.run(datetime(2020, 1, 1, 6, 00))
        self.assertFalse(var1.get())
