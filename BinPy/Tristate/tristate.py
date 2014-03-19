from BinPy.Gates import *

def tristate_logic(in_states):
    if in_states[1] == 0:
        return 2
    elif in_states[1] == 1:
        return in_states[0]
    else:
        return 3

def Buffer(*args):
    return Gate(tristate_logic, 2, 2, *args)


# Useful to implement output enable in ICs
class Bus(object):
    def __init__(self, *args):
        self.b = None
        self._args = args
        self.inputs = []
        self.outputs = []
        self._check_args()

    def _check_args(self):
        pass



