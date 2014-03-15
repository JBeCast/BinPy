from BinPy.Gates import *

class Buffer(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 2, *args)

    def _calc_output(self, in_states):
        if self.inputs[1].state == 0:
            return 2
        elif self.inputs[1].state == 1:
            return self.inputs[0].state
        else:
            return 3

# Useful to implement output enable in ICs
class Bus(object):
    pass



