import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.Compare import CompareGreaterThan


class CompareTest(unittest.TestCase):
    def test(self) -> None:
        executor = FlowExecutor()

        in1 = executor.var("test1", float, default=1)

        out = executor.var("out", bool)

        executor.add([
            CompareGreaterThan[float](in1, 2.0).to(out),
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 00))

        self.assertFalse(out.get())


if __name__ == '__main__':
    unittest.main()
