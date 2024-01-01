from myhdl import *

@block
def axi4sw(reset, clk, tDataIn, tValidIn, tReadyOut_o, tDataOut,tValidOut_o, tReadyIn, nWide=4):
    tReadyOut = Signal(True);
    tValidOut = Signal(False);
    currentWord = Signal(intbv(0, min=0, max = nWide*len(tDataIn)));
    
    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if tValidIn==1 and tReadyOut==1 and (not tValidOut) and (currentWord < nWide):
            tDataOut.next[(currentWord+1)*len(tDataIn):currentWord*len(tDataIn)] = tDataIn
            currentWord.next = currentWord+1
            if currentWord == nWide - 1:
                tReadyOut.next = 0
            else:
                tReadyOut.next = 1

        if currentWord == nWide:
            tValidOut.next = 1
            if tValidOut == 1 and tReadyIn == 1:
                tValidOut.next = 0
                currentWord.next = 0
                tReadyOut.next = 1
        
    return logic, out_reg
