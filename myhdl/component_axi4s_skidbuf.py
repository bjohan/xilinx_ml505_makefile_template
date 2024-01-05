from myhdl import *

@block
def axi4s_skidbuf(reset, clk, tDataIn, tValidIn, tReadyOut_o, tLastIn, tDataOut,tValidOut_o, tReadyIn, tLastOut):
    buf0 = Signal(intbv(0)[len(tDataIn):])
    lst0 = Signal(False)
    buf1 = Signal(intbv(0)[len(tDataIn):])
    lst1 = Signal(False)
    state = Signal(intbv(0, min = 0 , max = 3))
    transferIn = Signal(False)
    transferOut = Signal(False)
    tValidOut = Signal(False)
    tReadyOut = Signal(False)

    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferIn.next = tValidIn == 1 and tReadyOut == 1
        transferOut.next = tValidOut == 1 and tReadyIn == 1
        tDataOut.next = buf0
        tLastOut.next = lst0

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == 0:
            tReadyOut.next = 1
        if transferIn and not transferOut:
            if state == 0:
                buf0.next = tDataIn
                lst0.next = tLastIn
                state.next = 1
                tValidOut.next = 1
            if state == 1:
                buf1.next = tDataIn
                lst1.next = tLastIn
                state.next = 2
                tReadyOut.next = 0

        if transferOut and not transferIn:
            if state == 1:
                state.next = 0
                tValidOut.next = 0
            if state == 2:
                state.next = 1
                buf0.next = buf1
                lst0.next = lst1
                tReadyOut.next = 0

        if transferOut and transferIn:
            if state == 1:
                buf0.next = tDataIn
                lst0.next = tLastIn
             
        
    return logic, out_reg
