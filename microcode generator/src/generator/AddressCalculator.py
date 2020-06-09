class AddressCalculator:
    _stepOffset = 0
    _flagsOffset = 3
    _opCodeOffset = 6
    _stepMask = 0b0000000000111
    _flagsMask = 0b0000000111000
    _opCodeMask = 0b1111111000000

    def calculate_address(self, step, flags, opcode):
        address = (step << self._stepOffset) & self._stepMask
        address += (flags << self._flagsOffset) & self._flagsMask
        address += (opcode << self._opCodeOffset) & self._opCodeMask
        return address
