import unittest

from generator.MicrocodeRomBuilder import MicrocodeRomBuilder


class MicrocodeRomBuilderTests(unittest.TestCase):

    def test_capacity(self):
        builder = MicrocodeRomBuilder(100)
        self.assertEqual(builder.capacity, 100)

    def test_address(self):
        builder = MicrocodeRomBuilder(100)
        address = builder._calculate_address(3, 0b010, 3)
        self.assertEqual(address, 0b0000011010011)

    def test_address2(self):
        builder = MicrocodeRomBuilder(100)
        address = builder._calculate_address(0b111, 0b111, 0b1111111)
        self.assertEqual(address, 0b1111111111111)

    def test_address3(self):
        builder = MicrocodeRomBuilder(100)
        address = builder._calculate_address(0b101, 0b101, 0b1110111)
        self.assertEqual(address, 0b1110111101101)

    def test_setValue(self):
        builder = MicrocodeRomBuilder(0x1fff)
        builder.set_value(0b000, 0b000, 0b0000001, 42)
        address = builder._calculate_address(0b000, 0b000, 0b0000001)
        self.assertEqual(builder.data[address], 42)

    def test_setValue2(self):
        builder = MicrocodeRomBuilder(0x1fff)
        builder.set_value(0b001, 0b001, 0b0000011, 42)
        address = builder._calculate_address(0b001, 0b001, 0b0000011)
        self.assertEqual(builder.data[address], 42)

    def test_setValue3(self):
        builder = MicrocodeRomBuilder(0x2000)
        builder.set_value(0b111, 0b111, 0b1111111, 42)
        address = builder._calculate_address(0b111, 0b111, 0b1111111)
        self.assertEqual(builder.data[address], 42)

    def test_setValue0(self):
        builder = MicrocodeRomBuilder(0x1fff)
        builder.set_value(0, 0, 0, 42)
        address = builder._calculate_address(0, 0, 0)
        self.assertEqual(builder.data[address], 42)
