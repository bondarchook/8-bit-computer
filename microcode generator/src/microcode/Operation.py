from typing import List
from microcode.Step import Step


class Operation:
    name = ""
    steps: List[Step]

    def __init__(self, name):
        self.steps = []
        self.name = name

    def add_step(self, step: Step):
        self.steps.append(step)

    def __str__(self):
        return f'{self.name}: {self.steps.count()}'
