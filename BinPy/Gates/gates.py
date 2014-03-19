from BinPy.Gates.connector import *


class Gate(object):

    """
    This class creates any logic gate based on the received arguments.
     Parameters:
        logic: a function that takes the input states (integers) and
        returns the output state (also an integer). Input and output
        states must be valid: 0, 1, 2 or 3.
        min_inputs: minimum number of inputs expected.
        max_inputs: maximum number of inputs expected.
        *args: an optional string (gate's name), a number of Connector
        class instances between min_inputs and max_inputs (the gate's
        inputs) and a last instance for the output.
    """

    def __init__(self, logic, min_inputs, max_inputs, *args):
        self._logic = logic
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
        is_connector(*self._taps)

    def trigger(self):
        """
        Calls the _logic function to calculate the output state.
        Triggers the output connector if the output has changed.
        """
        in_states = [i() for i in self._taps[:-1]]
        if len(in_states) == 1: in_states = in_states[0]
        out_state = self._logic(in_states)
        if out_state != self._taps[-1]():
            self._taps[-1].set(out_state)

    def connect(self, *taps):
        """
        Takes a number of Connector class instances between min_inputs
        and max_inputs (the gate's inputs) and a last instance for the
        output and connects them to the gate.
        Warning: every previous connection will be lost.
        """
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
        """
        Removes every connection, updating both the gate and the
        connectors.
        Warning: this method will render the gate useless, call it
        want to cleanly remove it from the circuit.
        """
        for i in self._taps:
            if self in i.connections['output']:
                i.connections['output'].remove(self)
            if self in i.connections['input']:
                i.connections['input'].remove(self)
        self._taps = []

    def __call__(self):
        return self._taps[-1]()

    def getTaps(self):
        """
        Returns the names of the connectors tapped into the gate.
        """
        return [i.name for i in self._taps]

    def getStates(self):
        """
        Returns the states of the input and output connectors.
        """
        return [i() for i in self._taps]

    def setInputs(self, *states):
        """
        Takes as many valid states as input connectors the gate has
        and changes their states to the ones provided.
        """
        states = list(states)
        if len(states) != len(self._taps[:-1]):
            raise Exception("%d values expected" % len(self._taps[:-1]))
        for i in range(len(states)):
            self._taps[i].set(states[i])


# Logic functions

def and_logic(inputs):
    if 0 in inputs: return 0
    elif inputs.count(1) == len(inputs): return 1
    else: return 3

def or_logic(inputs):
    if 1 in inputs: return 1
    elif inputs.count(0) == len(inputs): return 0
    else: return 3

def xor_logic(inputs):
    if 2 in inputs or 3 in inputs: return 3
    else:
        return 1 if inputs.count(1) % 2 else 0

def not_logic(input):
    return abs(input-1) if input in (0, 1) else 3

def nand_logic(inputs):
    return not_logic(and_logic(inputs))

def nor_logic(inputs):
    return not_logic(or_logic(inputs))

def xnor_logic(inputs):
    return not_logic(xor_logic(inputs))


# Gate generating functions

def AND(*args):
    return Gate(and_logic, 2, 8, *args)

def OR(*args):
    return Gate(or_logic, 2, 8, *args)

def XOR(*args):
    return Gate(xor_logic, 2, 8, *args)

def NAND(*args):
    return Gate(nand_logic, 2, 8, *args)

def NOR(*args):
    return Gate(nor_logic, 2, 8, *args)

def XNOR(*args):
    return Gate(xnor_logic, 2, 8, *args)

def NOT(*args):
    return Gate(not_logic, 1, 1, *args)