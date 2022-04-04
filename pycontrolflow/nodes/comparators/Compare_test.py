import unittest

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.Compare import CompareGreaterThan


class CompareTest(unittest.TestCase):
    def test(self):
        executor = FlowExecutor()

        in1 = executor.var("test1", int, default=1)
        in2 = executor.var("test2", bool, default=2)

        out = executor.var("out", bool)

        executor.add([
            CompareGreaterThan(in1, 2).to(out),
        ])

        self.assertFalse(out.get())


if __name__ == '__main__':
    unittest.main()
