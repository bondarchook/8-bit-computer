import yaml
from microcode.MicrocodeSpecification import MicrocodeSpecification
from microcode.Operation import Operation
from microcode.Step import Step
from microcode.FlagsState import FlagsState


class MicrocodeSpecificationLoader:
    file_name = ""
    microcode_specification = MicrocodeSpecification()

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        with open(self.file_name, 'r') as stream:
            try:
                print("Loading specification...\n")
                doc = yaml.safe_load(stream)
                self.load_control_signals(doc)
                self.load_fetch_sequence(doc)
                self.load_operations(doc)
                self.load_end_sequence(doc)
                print("\nSpecification load completed.")
            except yaml.YAMLError as exc:
                print(exc)

    def load_control_signals(self, doc):
        print("Control signals:")
        control_signals = list(doc.get("control-signals").keys())
        for i in range(0, len(control_signals)):
            value = pow(2, i)
            self.microcode_specification.control_signals[control_signals[i]] = value
            print('  %s -> %s (%i)' % (control_signals[i].rjust(3), "{0:018b}".format(value), value))

    def load_fetch_sequence(self, doc):
        print("\nFetch sequence:")
        fetch_sequence_op = doc.get("fetch-sequence")
        fetch_sequence = self.load_operation(fetch_sequence_op, 'fetch-sequence')
        self.microcode_specification.fetch_sequence = fetch_sequence

    def load_end_sequence(self, doc):
        print("\nEnd sequence:")
        end_sequence_op = doc.get("end-sequence")
        end_sequence = self.load_operation(end_sequence_op, 'end-sequence')
        self.microcode_specification.end_sequence = end_sequence

    def load_operations(self, doc):
        print("\nOperations:")
        operations = doc.get("operations")
        for op_name in operations:
            print("%s:" % op_name)
            operation = self.load_operation(operations[op_name], op_name)
            self.microcode_specification.operations.append(operation)

    def load_operation(self, operation_doc, name):
        operation = Operation(name)

        if operation_doc is None:
            print("N/A")
            return None

        for s in operation_doc:
            step = Step()
            operation.add_step(step)
            self.parse_flags(step, str(s[0]))
            for sig in s[1:]:
                step.add_control_signal(sig)
            print('    {}'.format(str(step)))
        return operation

    @staticmethod
    def parse_flags(step: Step, flags):
        if flags == '0':
            step.z_flag = FlagsState.ZERO
            step.c_flag = FlagsState.ZERO
            step.n_flag = FlagsState.ZERO
        else:
            step.z_flag = FlagsState.parse(flags[0])
            step.c_flag = FlagsState.parse(flags[1])
            step.n_flag = FlagsState.parse(flags[2])
