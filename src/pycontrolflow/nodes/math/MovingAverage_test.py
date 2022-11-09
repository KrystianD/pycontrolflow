import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.math.MovingAverage import MovingAverage


class MovingAverageTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var = executor.memory("var", float, initial_value=0)
        out = executor.var("out", float)

        executor.add([
            MovingAverage(var, 0.5).to(out),
        ])

        var.set(1)
        executor.run(datetime(2020, 1, 1, 15, 0, 0))
        self.assertEqual(1, out.get())

        var.set(2)
        executor.run(datetime(2020, 1, 1, 15, 0, 1))
        self.assertEqual(1.5, out.get())

        var.set(2)
        executor.run(datetime(2020, 1, 1, 15, 0, 2))
        self.assertEqual(1.75, out.get())

        var.set(2)
        executor.run(datetime(2020, 1, 1, 15, 0, 3))
        self.assertEqual(1.875, out.get())


if __name__ == '__main__':
    unittest.main()
