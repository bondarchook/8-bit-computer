class MicrocodeRomBuilder:
    _stepOffset = 0
    _flagsOffset = 3
    _opCodeOffset = 6
    _stepMask = 0b0000000000111
    _flagsMask = 0b0000000111000
    _opCodeMask = 0b1111111000000

    capacity = 0
    data = []

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [0] * capacity

    def set_value(self, step, flags, opcode, value):
        address = self._calculate_address(step, flags, opcode)
        self.data[address] = value

    def _calculate_address(self, step, flags, opcode):
        address = (step << self._stepOffset) & self._stepMask
        address += (flags << self._flagsOffset) & self._flagsMask
        address += (opcode << self._opCodeOffset) & self._opCodeMask
        return address
