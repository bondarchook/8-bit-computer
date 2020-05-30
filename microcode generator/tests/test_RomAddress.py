import shutil
import unittest
import ddt
from generator.MicrocodeBuilder import MicrocodeBuilder


class ArgumentList(list):
    pass


def data_line(listIn, name):
    r = ArgumentList(listIn)
    setattr(r, "__name__", name)
    return r


def generate_all_addresses():
    _stepOffset = 0
    _flagsOffset = 3
    _opCodeOffset = 6
    result = []
    for op in range(0, 0b1111111+1):
        for flags in range(0, 0b111+1):
            for step in range(0, 0b111+1):
                offset = step << _stepOffset
                offset += flags << _flagsOffset
                offset += op << _opCodeOffset
                result.append(data_line([step, flags, op, offset], "addr_" + str(offset)))
    return result


@ddt.ddt
class RomAddressTest(unittest.TestCase):

    @ddt.data(*generate_all_addresses())
    def test_rom_address(self, value):
        step, flags, op, offset = value
        directory = "/tmp/hex_test"
        builder = MicrocodeBuilder(directory, "rom")
        builder.set_value(step, flags, op, 0b100000000100000011000000)
        builder.write()
        a_rom_data = self.read_rom_file("/tmp/hex_test/rom_A.hex")
        b_rom_data = self.read_rom_file("/tmp/hex_test/rom_B.hex")
        c_rom_data = self.read_rom_file("/tmp/hex_test/rom_C.hex")

        self.assertEqual(0b11000000, a_rom_data[offset])
        self.assertEqual(0b01000000, b_rom_data[offset])
        self.assertEqual(0b10000000, c_rom_data[offset])

        shutil.rmtree(directory)

    @staticmethod
    def read_rom_file(file_name):
        f = open(file_name, 'rb')
        data = bytearray(f.read())
        f.close()
        return data
