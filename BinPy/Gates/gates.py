from BinPy.Gates.connector import *


class Gate(object):

    """
    Base Class implementing all common functions used by Logic gates
    """

    def __init__(self, min_inputs, max_inputs, *args):
        self._taps = list(args)
        self.name = ''
        self._min_inputs = min_inputs
        self._max_inputs = max_inputs
        self._check_taps()
        self.connect(*self._taps)

    def _check_taps(self):
        if isinstance(self._taps[0], str):
            self.name = self._taps[0]
            self._taps = self._taps[1:]
        for i in self._taps:
            is_connector(i)

    def trigger(self):
        in_states = [i() for i in self._taps[:-1]]
        out_state = self._calc_output(in_states)
        if out_state != self._taps[-1]():
            self._taps[-1].set(out_state)

    def connect(self, *taps):
        taps = list(taps)
        if taps[-1] in taps[:-1]:
            raise Exception("Gate feedback not allowed")
        if not self._min_inputs <= len(taps[:-1]) <= self._max_inputs:
            raise Exception("Unexpected number of inputs")
        if taps != self._taps:
            self.disconnect()
        self._taps = taps
        self._taps[-1].tap(self, 'output')
        for i in self._taps[:-1]:
            i.tap(self, 'input')
        self.trigger()

    def disconnect(self):
        for i in self._taps:
            if self in i.connections['output']:
                i.connections['output'].remove(self)
            if self in i.connections['input']:
                i.connections['input'].remove(self)
        self._taps = []

    def info(self):
        print "inputs:", ["%s(%d)" %(i.name, i()) for i in self._taps[:-1]]
        print "output:", "%s(%d)" %(self._taps[-1].name, self._taps[-1]())


# GATE ALGORITHMS

def and_alg(inputs):
    if 0 in inputs: return 0
    elif inputs.count(1) == len(inputs): return 1
    else: return 3

def or_alg(inputs):
    if 1 in inputs: return 1
    elif inputs.count(0) == len(inputs): return 0
    else: return 3

def xor_alg(inputs):
    if 2 in inputs or 3 in inputs: return 3
    else:
        return 1 if inputs.count(1) % 2 else 0


class AND(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        return and_alg(in_states)


class OR(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        return or_alg(in_states)


class NOT(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 1, 1, *args)

    def _calc_output(self, in_states):
        return abs(in_states[0]-1) if in_states[0] in (0,1) else 3


class NAND(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        temp = and_alg(in_states)
        return abs(temp-1) if temp in (0,1) else temp


class NOR(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        temp = or_alg(in_states)
        return abs(temp-1) if temp in (0,1) else temp


class XOR(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        return xor_alg(in_states)


class XNOR(Gate):
    def __init__(self, *args):
        Gate.__init__(self, 2, 8, *args)

    def _calc_output(self, in_states):
        temp = xor_alg(in_states)
        return abs(temp-1) if temp in (0,1) else temp