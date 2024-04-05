from myhdl import *
from interface_axi4s import Axi4sInterface
from component_axi4s_skidbuf import axi4s_skidbuf_no_last
from component_axi4s_connect import axi4s_connect_no_last

@block
def rs232tx(reset, clk, i, txd, baudDiv=100):
    txReady = Signal(True)
    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=11));
    completeWord = Signal(intbv(0, min=0, max=1024))

    ib = Axi4sInterface(len(i.data), withLast=False)
    i_skidbuf = axi4s_skidbuf_no_last(reset, clk, i, ib)
    #i_skidbuf = axi4s_connect_no_last(i, ib)

    @always_comb
    def out_reg():
        ib.ready.next = txReady

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            if currentBit > 0:
                baudCnt.next = baudCnt +1;
                if baudCnt == baudDiv:
                    baudCnt.next = 0
                    baudTick.next = True
                else:
                    baudTick.next = False

            if currentBit == 0 and ib.valid and txReady:
                txReady.next = False;
                currentBit.next = 1
                #completeWord.next[0] = 0; #start bit
                #completeWord.next[9:1] = ib.data;
                #completeWord.next[9] = 1; #stop bit
                completeWord.next[8:0] = ib.data;
                completeWord.next[8] = 1; #stop bit
                txd.next = 0 #start bit
            elif currentBit > 0 and currentBit < 10 and baudTick:
                txd.next = completeWord[0]
                completeWord.next = completeWord >> 1;
                #txd.next = completeWord[currentBit]
                currentBit.next = currentBit + 1
            elif currentBit == 10 and baudTick:
                currentBit.next = 0
                txReady.next = True
                txd.next = 1
            #elif currentBit == 0:
            #    txReady.next = True
            #    txd.next = 1

    return logic, out_reg, i_skidbuf
