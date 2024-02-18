from myhdl import *

@block
def rs232tx(reset, clk, i, txd, baudDiv=100):
    txReady = Signal(False)
    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=11));
    completeWord = Signal(intbv(0, min=0, max=1024))
    @always_comb
    def out_reg():
        i.ready.next = txReady

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

            if currentBit == 0 and i.valid and txReady:
                txReady.next = False;
                currentBit.next = 1
                completeWord.next[0] = 0; #start bit
                completeWord.next[9:1] = i.data;
                completeWord.next[9] = 1; #stop bit
                txd.next = 0 #start bit
            elif currentBit > 0 and currentBit < 10 and baudTick:
                txd.next = completeWord[currentBit]
                currentBit.next = currentBit + 1
            elif currentBit == 10 and baudTick:
                currentBit.next = 0
                txReady.next = True
                txd.next = 1
            elif currentBit == 0:
                txReady.next = True
                txd.next = 1

    return logic, out_reg
