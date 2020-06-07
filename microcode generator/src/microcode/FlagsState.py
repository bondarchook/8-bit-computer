from enum import Enum, unique


@unique
class FlagsState(Enum):
    ONE = 1
    ZERO = 0
    ANY = 'X'

    @staticmethod
    def parse(value):
        if value == "0":
            return FlagsState.ZERO
        if value == "1":
            return FlagsState.ONE
        if value == "X":
            return FlagsState.ANY
        raise ValueError('Can not map "%s" to FlagState. Allowed values "1", "0", "X"' % value)

    def __str__(self):
        if self.value == 0:
            return "0"
        if self.value == 1:
            return "1"
        if self.value == "X":
            return "X"
