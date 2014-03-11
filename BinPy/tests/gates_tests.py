from BinPy.Gates.gates import *
from nose.tools import with_setup, nottest


inputLogic = [(0, 0), (1, 0), (1, 1), (0, 1)]

def AND_test():
    c = [Connector() for i in range(3)]
    g = AND(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(c[0].state)
    if outputLogic != [0, 0, 1, 0]:
        assert False

def OR_test():
    c = [Connector() for i in range(3)]
    g = OR(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(c[0].state)
    if outputLogic != [0, 1, 1, 1]:
        assert False

def NAND_test():
    # Output connector state can also be accessed through the gate's output
    c = [Connector() for i in range(3)]
    g = NAND(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(g.output.state)
    if outputLogic != [1, 1, 0, 1]:
        assert False

def NOR_test():
    c = [Connector() for i in range(3)]
    g = NOR(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(c[0].state)
    if outputLogic != [1, 0, 0, 0]:
        assert False

def XOR_test():
    c = [Connector() for i in range(3)]
    g = XOR(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(c[0].state)
    if outputLogic != [0, 1, 0, 1]:
        assert False

def XNOR_test():
    c = [Connector() for i in range(3)]
    g = XNOR(*c)
    outputLogic = []

    for logic in inputLogic:
        c[1].set(logic[0])
        c[2].set(logic[1])
        outputLogic.append(c[0].state)
    if outputLogic != [1, 0, 1, 0]:
        assert False
