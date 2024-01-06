from myhdl import *

@block
def axi4sw(reset, clk, tDataIn, tValidIn, tReadyOut_o, tLastIn, tDataOut,tValidOut_o, tReadyIn, tLastOut, nWide=4):
    tReadyOut = Signal(True)
    tValidOut = Signal(False)
    currentWord = Signal(intbv(0, min=0, max = nWide*len(tDataIn)))
    transferIn = Signal(False)
    transferOut = Signal(False)
 
    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferIn.next = tValidIn and tReadyOut
        transferOut.next = tValidOut and tReadyIn
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if transferIn and (not tValidOut) and (currentWord < nWide):
            tDataOut.next[(currentWord+1)*len(tDataIn):currentWord*len(tDataIn)] = tDataIn
            currentWord.next = currentWord+1
            if currentWord == nWide - 1:
                tReadyOut.next = 0
                tValidOut.next = 1
                tLastOut.next = tLastIn
            else:
                tReadyOut.next = 1

        if currentWord == nWide:
            if transferOut:
                tValidOut.next = 0
                currentWord.next = 0
                tReadyOut.next = 1
                tLastOut.next = 0
        
    return logic, out_reg
