import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.comparators.Compare import CompareGreaterThan, CompareGreaterEqualTo, CompareLessThan, \
    CompareLessEqualTo


class CompareTest(unittest.TestCase):
    def test(self) -> None:
        executor = FlowExecutor()

        in1 = executor.var("test1", int, default=1)
        out1 = executor.var("out1", bool)
        out2 = executor.var("out2", bool)
        out3 = executor.var("out3", bool)
        out4 = executor.var("out4", bool)
        out5 = executor.var("out5", bool)
        out6 = executor.var("out6", bool)
        out7 = executor.var("out7", bool)
        out8 = executor.var("out8", bool)
        out9 = executor.var("out9", bool)
        out10 = executor.var("out10", bool)
        out11 = executor.var("out11", bool)
        out12 = executor.var("out12", bool)
        out13 = executor.var("out13", bool)

        executor.add([
            CompareGreaterThan[int](in1, 0).to(out1),
            CompareGreaterThan[int](in1, 1).to(out2),
            CompareGreaterThan[int](in1, 2).to(out3),
            CompareGreaterEqualTo[int](in1, 0).to(out4),
            CompareGreaterEqualTo[int](in1, 1).to(out5),
            CompareGreaterEqualTo[int](in1, 2).to(out6),
            CompareLessThan[int](in1, 0).to(out7),
            CompareLessThan[int](in1, 1).to(out8),
            CompareLessThan[int](in1, 2).to(out9),
            CompareLessEqualTo[int](in1, 0).to(out10),
            CompareLessEqualTo[int](in1, 1).to(out11),
            CompareLessEqualTo[int](in1, 2).to(out12),
            CompareLessEqualTo[int](in1, 2, invert=True).to(out13),
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertTrue(out1.get())
        self.assertFalse(out2.get())
        self.assertFalse(out3.get())
        self.assertTrue(out4.get())
        self.assertTrue(out5.get())
        self.assertFalse(out6.get())
        self.assertFalse(out7.get())
        self.assertFalse(out8.get())
        self.assertTrue(out9.get())
        self.assertFalse(out10.get())
        self.assertTrue(out11.get())
        self.assertTrue(out12.get())
        self.assertFalse(out13.get())

    def test_invalid_type(self) -> None:
        executor = FlowExecutor()

        in1 = executor.var("test1", int, default=1)
        out = executor.var("out", bool)

        with self.assertRaises(TypeError):
            executor.add([
                CompareLessEqualTo[int](in1, True).to(out),
            ])
