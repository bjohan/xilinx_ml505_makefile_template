from myhdl import *

@block
def axi4sn(reset, clk, tDataIn, tValidIn, tReadyOut_o, tDataOut,tValidOut_o, tReadyIn, nWide=4):
    tReadyOut = Signal(False);
    tValidOut = Signal(False);
    transferIn = Signal(False); 
    transferOut = Signal(False); 
    currentWord = Signal(intbv(0, min=0, max = nWide*len(tDataOut)));
    
    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferIn.next = tValidIn and tReadyOut
        transferOut.next = tValidOut and tReadyIn

    @always_seq(clk.posedge, reset=reset)
    def logic():
        
        tReadyOut.next = 0
        if tValidOut == 0:
            if tValidIn == 1:
                tDataOut.next = tDataIn[(currentWord+1)*len(tDataOut):currentWord*len(tDataOut)]
                currentWord.next = currentWord+1
                tValidOut.next = 1

        if transferOut == 1:
            tDataOut.next = tDataIn[(currentWord+1)*len(tDataOut):currentWord*len(tDataOut)]
            tValidOut.next = 1
            currentWord.next = currentWord+1
            if currentWord == 4:
                tValidOut.next = 0
                tReadyOut.next = 1
            
        if transferIn == 1:
            tValidOut.next = 0
            currentWord.next = 0

        #if tValidIn==1:
        #    tDataOut.next = tDataIn[(currentWord+1)*len(tDataOut):currentWord*len(tDataOut)]
        #    tValidOut.next = 1
        #    tReadyOut.next = 0
        #    if tReadyIn:
        #        if currentWord < nWide :
        #            currentWord.next = currentWord+1
        #            tDataOut.next = tDataIn[(currentWord+1)*len(tDataOut):currentWord*len(tDataOut)]
        #            tValidOut.next = 1
        #        else:
        #            tValidOut.next = 0
        #            currentWord.next = 0
        #            tReadyOut.next = 1

        
    return logic, out_reg
