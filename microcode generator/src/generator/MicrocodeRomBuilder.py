from generator.AddressCalculator import AddressCalculator


class MicrocodeRomBuilder:

    _address_calculator = AddressCalculator()
    capacity = 0
    data = []

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [0] * capacity

    def set_value(self, step, flags, opcode, value):
        address = self._address_calculator.calculate_address(step, flags, opcode)
        self.data[address] = value

