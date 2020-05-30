import os

from generator.MicrocodeRomBuilder import MicrocodeRomBuilder


class DemoGenerator1:
    fileName = ""

    def __init__(self, filename):
        self.fileName = filename

    def write(self):
        b = 1
        builder = MicrocodeRomBuilder(0x2000)
        if os.path.exists(self.fileName):
            os.remove(self.fileName)
        file = open(self.fileName, "wb")
        for o in range(0, 0b1111111+1):
            for f in range(0, 0b111+1):
                for s in range(0, 0b111+1):
                    builder.set_value(o, s, f, o)
                    b = b << 1
                b = 1
        file.write(bytes(builder.data))
        file.close()


gen = DemoGenerator1("/home/jura/projects/hex_generator/test_op.hex")
gen.write()
print('Done.')
