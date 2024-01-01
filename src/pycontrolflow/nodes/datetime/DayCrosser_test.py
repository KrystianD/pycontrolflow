import json
import unittest
from datetime import datetime

from pycontrolflow.FlowExecutor import FlowExecutor
from pycontrolflow.nodes.datetime.DayCrosser import DayCrosser


class DayCrosserTest(unittest.TestCase):
    def test_basic(self) -> None:
        executor = FlowExecutor()

        test1 = executor.var("test1", bool)

        executor.add([
            DayCrosser(persistent=True, nid="dc").to(test1),
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertFalse(test1.get())
        executor.run(datetime(2020, 1, 1, 16, 0, 00))
        self.assertFalse(test1.get())

        executor.run(datetime(2020, 1, 2, 7, 0, 00))
        self.assertTrue(test1.get())
        executor.run(datetime(2020, 1, 2, 9, 0, 00))
        self.assertFalse(test1.get())

        state = executor.serialize_state()
        # print(executor.serialize_state())

        self.assertEqual('{"_node.dc.date": "2020-01-02T09:00:00"}', json.dumps(state))

    def test_custom_time(self) -> None:
        executor = FlowExecutor()

        test1 = executor.var("test1", bool)

        executor.add([
            DayCrosser("06:00", persistent=True, nid="dc").to(test1),
        ])

        executor.run(datetime(2020, 1, 1, 15, 0, 00))
        self.assertFalse(test1.get())

        executor.run(datetime(2020, 1, 1, 17, 0, 00))
        self.assertFalse(test1.get())

        executor.run(datetime(2020, 1, 1, 23, 0, 00))
        self.assertFalse(test1.get())

        executor.run(datetime(2020, 1, 2, 4, 0, 00))
        self.assertFalse(test1.get())

        executor.run(datetime(2020, 1, 2, 7, 0, 00))
        self.assertTrue(test1.get())

        executor.run(datetime(2020, 1, 2, 9, 0, 00))
        self.assertFalse(test1.get())

        state = executor.serialize_state()
        # print(executor.serialize_state())

        self.assertEqual('{"_node.dc.date": "2020-01-02T09:00:00"}', json.dumps(state))
