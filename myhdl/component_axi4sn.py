from myhdl import *

@block
def axi4sn(reset, clk, i, o, nWide=4):
    tReadyOut = Signal(False);
    tValidOut = Signal(False);
    transferIn = Signal(False); 
    transferOut = Signal(False); 
    currentWord = Signal(intbv(0, min=0, max = nWide*len(o.data)));
    
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferIn.next = i.valid and tReadyOut
        transferOut.next = tValidOut and o.ready

    @always_seq(clk.posedge, reset=reset)
    def logic():
        
        tReadyOut.next = 0
        if tValidOut == 0:
            o.last.next = 0
            if i.valid == 1:
                o.data.next = i.data[(currentWord+1)*len(o.data):currentWord*len(o.data)]
                currentWord.next = currentWord+1
                tValidOut.next = 1

        if transferOut == 1:
            o.data.next = i.data[(currentWord+1)*len(o.data):currentWord*len(o.data)]
            tValidOut.next = 1
            currentWord.next = currentWord+1
            if currentWord == 3:
                o.last.next = i.last
            if currentWord == 4:
                tValidOut.next = 0
                tReadyOut.next = 1
                o.last.next = 0
            
        if transferIn == 1:
            tValidOut.next = 0
            currentWord.next = 0

    return logic, out_reg
