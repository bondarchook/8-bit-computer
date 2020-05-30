import os
import shutil
import unittest

from generator.MicrocodeBuilder import MicrocodeBuilder


class MicrocodeBuilderTests(unittest.TestCase):

    def test_parameters(self):
        builder = MicrocodeBuilder("dir", "file")
        self.assertEqual(builder.output_directory, "dir")
        self.assertEqual(builder.base_filename, "file")

    def test_file_creation(self):
        directory = "/tmp/hex_test"
        builder = MicrocodeBuilder(directory, "rom")
        builder.set_value(0, 0, 0, 1)
        builder.write()
        self.assertTrue(os.path.exists("/tmp/hex_test/rom_A.hex"))
        self.assertTrue(os.path.exists("/tmp/hex_test/rom_B.hex"))
        self.assertTrue(os.path.exists("/tmp/hex_test/rom_C.hex"))

        self.assertEqual(os.path.getsize("/tmp/hex_test/rom_A.hex"), 0x2000)
        self.assertEqual(os.path.getsize("/tmp/hex_test/rom_B.hex"), 0x2000)
        self.assertEqual(os.path.getsize("/tmp/hex_test/rom_C.hex"), 0x2000)

        shutil.rmtree(directory)

    def test_set_value(self):
        self.assertFalse(False)