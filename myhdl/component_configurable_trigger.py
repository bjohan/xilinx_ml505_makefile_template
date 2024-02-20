from myhdl import *

@block
def configurable_trigger(reset, clk, dataIn, compare, care, trigged):
    dataInR = Signal(modbv(0)[len(dataIn):])
    toCompare = Signal(modbv(0)[len(dataIn):])
    @always_comb
    def trig():
        #toCompare.next = dataIn
        for i in range(len(dataIn)):
            toCompare.next[i] = (dataIn[i] == compare[i]) and care[i]
        trigged.next = toCompare == care

    @always_seq(clk.posedge, reset=reset)
    def logic():
        dataInR.next = dataIn

    return trig,logic
