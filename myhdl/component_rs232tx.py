from myhdl import *

@block
def rs232tx(reset, toTx, txValid, txReadyOut, txBusy, txd, clk, baudDiv=100):
    txReady = Signal(False)
    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=11));
    completeWord = Signal(intbv(0, min=0, max=1024))
    @always_comb
    def out_reg():
        txReadyOut.next = txReady

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            if currentBit > 0:
                txBusy.next =True
                baudCnt.next = baudCnt +1;
                if baudCnt == baudDiv:
                    baudCnt.next = 0
                    baudTick.next = True
                else:
                    baudTick.next = False
            else:
                txBusy.next = False

            if currentBit == 0 and txValid and txReady:
                txReady.next = False;
                currentBit.next = 1
                completeWord.next[0] = 0; #start bit
                completeWord.next[9:1] = toTx;
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
        #else:
        #    baudTick.next = 0
        #    baudCnt.next = 0
        #    currentBit.next = 0
        #    completeWord.next = 0
        #    txReady.next = 1
        #    txBusy.next = 0


    return logic, out_reg
