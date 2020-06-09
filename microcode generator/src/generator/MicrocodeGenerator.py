from generator.AddressCalculator import AddressCalculator
from generator.MicrocodeBuilder import MicrocodeBuilder
from microcode.MicrocodeSpecification import MicrocodeSpecification
from microcode.FlagsState import FlagsState


class MicrocodeGenerator:

    _address_calculator = AddressCalculator()
    output_directory = ""
    base_filename = ""
    builder: MicrocodeBuilder
    spec: MicrocodeSpecification
    signals = None

    def __init__(self, output_directory, base_filename, spec: MicrocodeSpecification):
        self.output_directory = output_directory
        self.base_filename = base_filename
        self.builder = MicrocodeBuilder(output_directory, base_filename)
        self.spec = spec
        self.signals = spec.control_signals

    def generate(self):
        print("Generating ROM in '{}' name: {}".format(self.output_directory, self.base_filename))
        op_index = 0
        for operation in self.spec.operations:
            print("\n{} ({})".format(operation.name, op_index))
            step_index = 0
            step_index = self.generate_steps(op_index, step_index, self.spec.fetch_sequence.steps)
            step_index = self.generate_steps(op_index, step_index, operation.steps)
            self.generate_steps(op_index, step_index, self.spec.end_sequence.steps)
            op_index += 1
        self.builder.write()

    def generate_steps(self, op_index, step_index, steps):
        for step in steps:
            control_word = self.calculate_control_word(step)
            self.expand_steps(step, step_index, op_index, control_word)
            step_index += 1
        return step_index

    def calculate_control_word(self, step):
        control_word = 0
        for sig in step.control_word:
            control_word += self.signals[sig]
        return control_word

    def expand_steps(self, step, step_index, op_index, control_word):
        for zf in self.flag_to_range(step.z_flag):
            for cf in self.flag_to_range(step.c_flag):
                for nf in self.flag_to_range(step.n_flag):
                    flags = (zf << 2) + (cf << 1) + nf
                    self.builder.set_value(step_index, flags, op_index, control_word)
                    self.print(step_index, flags, op_index, control_word)

    @staticmethod
    def flag_to_range(flag: FlagsState):
        if flag == FlagsState.ZERO:
            return [0]
        if flag == FlagsState.ONE:
            return [1]
        if flag == FlagsState.ANY:
            return [0, 1]

    def print(self, step_index, flags, op_index, control_word):
        address = self._address_calculator.calculate_address(step_index, flags, op_index)
        a = (control_word & 0b000000000000000011111111) >> 0
        b = (control_word & 0b000000001111111100000000) >> 8
        c = (control_word & 0b111111110000000000000000) >> 16
        print("{0:07b} {1:03b} {2:03b} ({3: 4X}) -> {4:018b} [{5:2X} {6:2X} {7:2X}] ({8:5X})"
              .format(op_index, flags, step_index, address, control_word, a, b, c, control_word))