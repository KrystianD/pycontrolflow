import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.Changed import Changed


class ChangedTest(unittest.TestCase):
    def test(self) -> None:
        executor = FlowExecutor()

        in1 = executor.memory("test1", int, initial_value=1)
        out = executor.var("out", bool)

        executor.add([
            Changed[int](in1).to(out),
        ])

        in1.set(1)
        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertFalse(out.get())

        in1.set(1)
        executor.run(datetime(2020, 1, 1, 15, 1, 00))
        self.assertFalse(out.get())

        in1.set(2)
        executor.run(datetime(2020, 1, 1, 15, 2, 00))
        self.assertTrue(out.get())


if __name__ == '__main__':
    unittest.main()
