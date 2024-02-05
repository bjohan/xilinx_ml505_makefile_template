from myhdl import *

@block
def configurable_trigger(dataIn, andMask, orMask, triggedAnd, triggedOr):

    @always_comb
    def trig_and():
        x = dataIn[0] and  andMask[0]
        for i in range(len(dataIn)-1):
            x = x and ((dataIn[i+1] and andMask[i+1])  or( not andMask[i+1]))
        triggedAnd.next = x

    @always_comb
    def trig_or():
        x = dataIn[0] or  orMask[0]
        for i in range(len(dataIn)-1):
            x = x or (dataIn[i+1] and orMask[i+1])
        triggedOr.next = x

    return trig_and, trig_or
