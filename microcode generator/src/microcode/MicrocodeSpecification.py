from typing import List
from microcode.Operation import Operation


class MicrocodeSpecification:
    control_signals: dict
    fetch_sequence: Operation
    operations: List[Operation]
    end_sequence: Operation

    def __init__(self):
        self.control_signals = dict()
        self.operations = []
