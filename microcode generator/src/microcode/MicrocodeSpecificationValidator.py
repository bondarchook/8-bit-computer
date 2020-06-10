from microcode.MicrocodeSpecification import MicrocodeSpecification


class MicrocodeSpecificationValidator:

    @staticmethod
    def validate(spec: MicrocodeSpecification):
        available_control_signals = spec.control_signals
        MicrocodeSpecificationValidator.validate_operation(available_control_signals, spec.fetch_sequence)
        for op in spec.operations:
            MicrocodeSpecificationValidator.validate_operation(available_control_signals, op)
        print("Specification is valid.")

    @staticmethod
    def validate_operation(available_control_signals, operation):
        step_index = 0

        if operation is None:
            return

        for step in operation.steps:
            step_index += 1
            sig_index = 0
            for sig in step.control_word:
                sig_index += 1
                if not (sig in available_control_signals):
                    raise ValueError(f'{operation.name}[{step_index}, {sig_index}] -> "{sig}" Unexpected control signal.')
