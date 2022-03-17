import unittest
from datetime import datetime, timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.timers.CountingTimer import CountingTimer


class CountingTimerTest(unittest.TestCase):
    def test1(self):
        executor = FlowExecutor()

        var = executor.memory("var", bool)
        out = executor.var("out", bool)

        executor.add([
            CountingTimer(var, timedelta(seconds=7)).to(out),
        ])

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 0))
        self.assertFalse(out.get())

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 5))
        self.assertFalse(out.get())

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 10))
        self.assertTrue(out.get())

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 15))
        self.assertTrue(out.get())

        var.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 17))
        self.assertFalse(out.get())

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 20))
        self.assertFalse(out.get())

        var.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 35))
        self.assertTrue(out.get())


if __name__ == '__main__':
    unittest.main()
