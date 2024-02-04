from myhdl import *

@block
def axi4sw(reset, clk, i, o, nWide=4):
    tReadyOut = Signal(True)
    tValidOut = Signal(False)
    currentWord = Signal(intbv(0, min=0, max = nWide*len(i.data)))
    transferIn = Signal(False)
    transferOut = Signal(False)
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferIn.next = i.valid and tReadyOut
        transferOut.next = tValidOut and o.ready
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if transferIn and (not tValidOut) and (currentWord < nWide):
            o.data.next[(currentWord+1)*len(i.data):currentWord*len(i.data)] = i.data
            currentWord.next = currentWord+1
            if currentWord == nWide - 1:
                tReadyOut.next = 0
                tValidOut.next = 1
                o.last.next = i.last
            else:
                tReadyOut.next = 1

        if currentWord == nWide:
            if transferOut:
                tValidOut.next = 0
                currentWord.next = 0
                tReadyOut.next = 1
                o.last.next = 0
        
    return logic, out_reg
