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


@ddt.ddt
class RomValuesTest(unittest.TestCase):

    @ddt.data(
        data_line([1, 0, 0, 1], 'Test_case_1'),
        data_line([100, 0, 0, 100], 'Test_case_2'),
        data_line([0b000000000000000111111111, 0b00000000, 0b00000001, 0b11111111], 'Test_case_3'),
        data_line([0b000000011111111111111111, 0b00000001, 0b11111111, 0b11111111], 'Test_case_4'),
        data_line([0b100000000100000011000000, 0b10000000, 0b01000000, 0b11000000], 'Test_case_5'),
        data_line([0b000000010000001000000011, 0b00000001, 0b00000010, 0b00000011], 'Test_case_6'),
        data_line([0b101010101010101010101010, 0b10101010, 0b10101010, 0b10101010], 'Test_case_7'),
        data_line([0b010101010101010101010101, 0b01010101, 0b01010101, 0b01010101], 'Test_case_8'),
        data_line([0b111111111111111111111111, 0b11111111, 0b11111111, 0b11111111], 'Test_case_all_1'),
        data_line([0b000000000000000000000000, 0b00000000, 0b00000000, 0b00000000], 'Test_case_all_0'),
    )
    def test_rom_value(self, value):
        v, c, b, a = value
        directory = "/tmp/hex_test"
        builder = MicrocodeBuilder(directory, "rom")
        builder.set_value(0, 0, 0, v)
        builder.write()
        a_rom_data = self.read_rom_file("/tmp/hex_test/rom_A.hex")
        b_rom_data = self.read_rom_file("/tmp/hex_test/rom_B.hex")
        c_rom_data = self.read_rom_file("/tmp/hex_test/rom_C.hex")

        self.assertEqual(a, a_rom_data[0])
        self.assertEqual(b, b_rom_data[0])
        self.assertEqual(c, c_rom_data[0])

        shutil.rmtree(directory)

    @staticmethod
    def read_rom_file(file_name):
        f = open(file_name, 'rb')
        data = bytearray(f.read())
        f.close()
        return data
