import os

from generator.MicrocodeRomBuilder import MicrocodeRomBuilder


class MicrocodeBuilder:
    _aPartMask = 0b000000000000000011111111
    _bPartMask = 0b000000001111111100000000
    _cPartMask = 0b111111110000000000000000
    _aPartOffset = 0
    _bPartOffset = 8
    _cPartOffset = 16
    _romCapacity = 0x2000

    output_directory = ""
    base_filename = ""

    _romA = MicrocodeRomBuilder(_romCapacity)
    _romB = MicrocodeRomBuilder(_romCapacity)
    _romC = MicrocodeRomBuilder(_romCapacity)

    def __init__(self, output_directory, base_filename):
        self.output_directory = output_directory
        self.base_filename = base_filename

    def set_value(self, step, flags, opcode, value):
        a_part = (value & self._aPartMask) >> self._aPartOffset
        b_part = (value & self._bPartMask) >> self._bPartOffset
        c_part = (value & self._cPartMask) >> self._cPartOffset

        self._romA.set_value(step, flags, opcode, a_part)
        self._romB.set_value(step, flags, opcode, b_part)
        self._romC.set_value(step, flags, opcode, c_part)

    def write(self):
        self.write_file("A", self._romA.data)
        self.write_file("B", self._romB.data)
        self.write_file("C", self._romC.data)

    def write_file(self, suffix, data):
        file_name = self.base_filename + "_" + suffix + ".hex"
        full_file_name = os.path.join(self.output_directory, file_name)

        if os.path.exists(full_file_name):
            os.remove(full_file_name)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory, exist_ok=True)

        file = open(full_file_name, "wb")
        file.write(bytes(data))
        file.close()
