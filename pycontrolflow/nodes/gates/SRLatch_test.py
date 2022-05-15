import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.gates.DFlipFlop import DFlipFlop
from pycontrolflow.nodes.gates.SRLatch import SRLatch


class Test(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        var_s = executor.memory("var_s", bool, initial_value=False)
        var_r = executor.memory("var_r", bool, initial_value=False)
        var_out = executor.var("out", bool)

        executor.add([
            SRLatch(var_s, var_r).to(var_out)
        ])

        def tick(set: bool, reset: bool, expected_value: bool) -> None:
            var_s.set(set)
            var_r.set(reset)
            executor.run(datetime.now())
            self.assertEqual(expected_value, var_out.get())

        tick(set=True, reset=False, expected_value=True)
        tick(set=True, reset=False, expected_value=True)
        tick(set=False, reset=False, expected_value=True)
        tick(set=False, reset=True, expected_value=False)
        tick(set=False, reset=True, expected_value=False)
        tick(set=False, reset=False, expected_value=False)
        tick(set=False, reset=False, expected_value=False)


if __name__ == '__main__':
    unittest.main()
