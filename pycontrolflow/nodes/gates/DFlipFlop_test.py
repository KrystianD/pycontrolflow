import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.gates.DFlipFlop import DFlipFlop


class Test(unittest.TestCase):
    def test1(self):
        executor = FlowExecutor()

        var_d = executor.memory("var_d", bool)
        var_c = executor.memory("var_c", bool)
        var_out = executor.var("out", bool)

        executor.add([
            DFlipFlop(var_d, var_c).to(var_out)
        ])

        def tick(value, clock, expected_value):
            var_d.set(value)
            var_c.set(clock)
            executor.run(datetime.now())
            self.assertEqual(expected_value, var_out.get())

        tick(value=True, clock=False, expected_value=False)
        tick(value=True, clock=True, expected_value=True)
        tick(value=True, clock=False, expected_value=True)
        tick(value=False, clock=False, expected_value=True)
        tick(value=False, clock=True, expected_value=False)
        tick(value=False, clock=True, expected_value=False)
        tick(value=False, clock=False, expected_value=False)

        tick(value=False, clock=True, expected_value=False)
        tick(value=True, clock=True, expected_value=False)
        tick(value=False, clock=True, expected_value=False)


if __name__ == '__main__':
    unittest.main()
