pycontrolflow
======

Python framework for easy control algorithms writing.
It can be seen as a combination of [Node-RED](https://nodered.org/) and PLC ladder programming.

Write algorithms in the declarative (telling systems what you want),
instead of the imperative way (telling systems what to do).

It is based on Nodes connected to each other via Variables forming a Flow.

## Features

* Many ready to use blocks,
* Persistence support,
* **Strong type checking both in runtime and with mypy checking**,
* Nulls not allowed,
* Fully testable - no dependency on the environment (date/time).

## Example use cases

* Controlling battery charging/discharging for solar installations,
* Battery maintenance state machine,
* Fault management,
* ... and much more!

## Example

See examples [here](examples/README.md).

## Concepts

* Flow - consists of Nodes that are executed in order,
* Node - performs some operations on its inputs, resulting in outputs, configured via parameters,
* Variable - holds data:
    * `var` - temporary variable for passing data out of the flow and to use between flow nodes
    * `memory` - variable that persists across flow executions, including passing data into the flow,
* Timers - performing time-related tasks:
  * One shot - sets its output to True if time elapses, triggered with its `trigger` variable, or reset with its `reset` variable,
    * Repeating - sets its output to True every time it elapses

## Nodes

### Comparators

* [Changed](src/pycontrolflow/nodes/comparators/Changed.py) - detects of variable change
* [Compare](src/pycontrolflow/nodes/comparators/Compare.py) - compares two variables
* [EdgeFalling](src/pycontrolflow/nodes/comparators/EdgeFalling.py) - detects condition change from True to False
* [EdgeRising](src/pycontrolflow/nodes/comparators/EdgeRising.py) - detects condition change from False to True
* [SchmittGate](src/pycontrolflow/nodes/comparators/SchmittGate.py) - gate with hysteresis
* [PreviousStateCondition](src/pycontrolflow/nodes/comparators/PreviousStateCondition.py) - base node for creating comparators

### Date/time utils

* [DayCrosser](src/pycontrolflow/nodes/datetime/DayCrosser.py) - detects the day change (with optional specific time)
* [TimeCheck](src/pycontrolflow/nodes/datetime/TimeCheck.py) - checks if current time is within range

### Flow control

* [If](src/pycontrolflow/nodes/flow_control/If.py) - branches flow depending on the condition

### Gates

* [DFlipFlop](src/pycontrolflow/nodes/gates/DFlipFlop.py) - edge-triggered D gate - [wiki](https://ecstudiosystems.com/discover/textbooks/basic-electronics/flip-flops/d-flip-flop/)
* [DLatch](src/pycontrolflow/nodes/gates/DLatch.py) - level-triggered D gate - [wiki](https://en.wikipedia.org/wiki/Flip-flop_(electronics)#Gated_D_latch)
* [SRLatch](src/pycontrolflow/nodes/gates/SRLatch.py) - level-triggered SR gate - [wiki](https://en.wikipedia.org/wiki/Flip-flop_(electronics)#Gated_SR_latch)

### Logic

* [And](src/pycontrolflow/nodes/logic/And.py) - logical AND on the inputs
* [Or](src/pycontrolflow/nodes/logic/Or.py) - logical OR on the inputs
* [Invert](src/pycontrolflow/nodes/logic/Invert.py) - logical NOT on the input
* [LogicOp](src/pycontrolflow/nodes/logic/LogicOp.py) - base node for creating logic operators

### Timers

* [TimerOnDelay](src/pycontrolflow/nodes/timers/TimerOnDelay.py) - enables its output if the input is True for specific amount of time (like PLC ON Timer)
* [TimerStop](src/pycontrolflow/nodes/timers/TimerStop.py) - stops running one-shot timer
* [TimerTrigger](src/pycontrolflow/nodes/timers/TimerTrigger.py) - triggers (or re-triggers) one-shot timer

### Util

* [ConditionMonitor](src/pycontrolflow/nodes/util/ConditionMonitor.py) - advanced condition monitor with an optional gap allowance
* [Debounce](src/pycontrolflow/nodes/util/Debounce.py) - limit change rate of a variable
* [Select](src/pycontrolflow/nodes/util/Select.py) - helper for selecting values based on input value
* [Startup](src/pycontrolflow/nodes/util/Startup.py) - outputs True only on the first Flow run
* [Transform](src/pycontrolflow/nodes/util/Transform.py) - transforms input values into output value using specified user function

### Values

* [Set](src/pycontrolflow/nodes/values/Set.py) - outputs True
* [Clear](src/pycontrolflow/nodes/values/Clear.py) - outputs False
* [Move](src/pycontrolflow/nodes/values/Move.py) - moves input to output
