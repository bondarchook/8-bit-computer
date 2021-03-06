from microcode.FlagsState import FlagsState


class Step:
    z_flag: FlagsState
    c_flag: FlagsState
    n_flag: FlagsState
    control_word: list

    def __init__(self):
        self.control_word = list()

    def add_control_signal(self, signal):
        self.control_word.append(signal)

    def __str__(self):
        control_words = ", ".join(self.control_word)
        return f'{str(self.z_flag)}{str(self.c_flag)}{str(self.n_flag)}: {control_words}'
