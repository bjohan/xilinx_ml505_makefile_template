from myhdl import *

@block
def configurable_trigger(dataIn, andMask, orMask, triggedAnd, triggedOr):

    @always_comb
    def trig_and():
        x = dataIn[0] and  andMask[0]
        for i in range(1, len(dataIn)):
            x = x and ((dataIn[i] and andMask[i])  or( not andMask[i]))
        triggedAnd.next = x

    @always_comb
    def trig_or():
        x = dataIn[0] or  orMask[0]
        for i in range(1, len(dataIn)):
            x = x or (dataIn[i] and orMask[i])
        triggedOr.next = x

    return trig_and, trig_or
