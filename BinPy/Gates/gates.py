from BinPy.Gates.connector import *


class Gate(object):

    """
    Base Class implementing all common functions used by Logic gates
    """

    def __init__(self, min_inputs, max_inputs, *args):
        self._args = list(args)
        self.name = ''
        self.inputs = []
        self.output = None
        self._min_inputs = min_inputs
        self._max_inputs = max_inputs
        self._check_args()
        self.connect(*self._args)

    def _check_args(self):
        if isinstance(self._args[0], str):
            self.name = self._args[0]
            self._args = self._args[1:]
        for i in self._args:
            is_connector(i)

    def trigger(self):
        in_states = [i() for i in self.inputs]
        out_state = self._calc_output(in_states)
        if out_state != self.output():
            self.output.set(out_state)

    def connect(self, *taps):
        inputs = list(taps)[:-1]
        output = list(taps)[-1]
        if output in inputs:
            raise Exception("Feedback not allowed")
        if not self._min_inputs <= len(inputs) <= self._max_inputs:
            raise Exception("Wrong number of inputs provided")
        self.disconnect()
        self.inputs = inputs
        self.output = output
        output.tap(self, 'output')
        for i in inputs:
            i.tap(self, 'input')
        self.trigger()

    def disconnect(self):
        if not self.output is None:
            if self in self.output.connections['output']:
                self.output.connections['output'].remove(self)
            if self in self.output.connections['input']:
                self.output.connections['input'].remove(self)
        for i in range(len(self.inputs)):
            if self in self.inputs[i].connections['input']:
                self.inputs[i].connections['input'].remove(self)
            if self in self.inputs[i].connections['output']:
                self.inputs[i].connections['output'].remove(self)
        self.inputs = []
        self.output = None

    def info(self):
        print "inputs:", ["%s(%d)" %(i.name, i()) for i in self.inputs]
        print "output:", "%s(%d)" %(self.output.name, self.output())



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