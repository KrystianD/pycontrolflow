import json
import unittest
from datetime import datetime, timedelta

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.util.ConditionMonitor import ConditionMonitor


class ConditionMonitorTest(unittest.TestCase):
    def test1(self) -> None:
        executor = FlowExecutor()

        test1 = executor.memory("test1", bool)
        test_met = executor.var("test_met", bool)
        test_met_time = executor.var("test_met_time", timedelta)

        executor.add([
            ConditionMonitor(test1, max_gap_time=timedelta(seconds=10), nid="nid1", persistent=True,
                             output_met=test_met,
                             output_met_time=test_met_time),
        ])

        test1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 0))
        self.assertTrue(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=0))

        test1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 5))
        self.assertTrue(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=5))

        test1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 10))
        self.assertTrue(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=10))

        test1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 20))
        self.assertFalse(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=0))

        test1.set(False)
        executor.run(datetime(2020, 1, 1, 15, 0, 25))
        self.assertFalse(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=0))

        test1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 30))
        self.assertTrue(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=0))

        test1.set(True)
        executor.run(datetime(2020, 1, 1, 15, 0, 35))
        self.assertTrue(test_met.get())
        self.assertEqual(test_met_time.get(), timedelta(seconds=5))

        state = executor.serialize_state()
        # print(executor.serialize_state())

        self.assertEqual('{"met_start": "2020-01-01T15:00:30", "last_met_date": "2020-01-01T15:00:35"}', json.dumps(state))


if __name__ == '__main__':
    unittest.main()
