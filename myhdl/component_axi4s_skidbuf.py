from myhdl import *

@block
def axi4s_skidbuf(reset, clk, i, o):
    buf0 = Signal(intbv(0)[len(i.data):])
    lst0 = Signal(False)
    buf1 = Signal(intbv(0)[len(i.data):])
    lst1 = Signal(False)
    state = Signal(intbv(0, min = 0 , max = 3))
    transferIn = Signal(False)
    transferOut = Signal(False)
    tValidOut = Signal(False)
    tReadyOut = Signal(False)

    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferIn.next = i.valid == 1 and tReadyOut == 1
        transferOut.next = tValidOut == 1 and o.ready == 1
        o.data.next = buf0
        o.last.next = lst0

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == 0:
            tReadyOut.next = 1
        if transferIn and not transferOut:
            if state == 0:
                buf0.next = i.data
                lst0.next = i.last
                state.next = 1
                tValidOut.next = 1
            if state == 1:
                buf1.next = i.data
                lst1.next = i.last
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
                buf0.next = i.data
                lst0.next = i.last
             
        
    return logic, out_reg


@block
def axi4s_skidbuf_no_last(reset, clk, i, o):
    buf0 = Signal(intbv(0)[len(i.data):])
    buf1 = Signal(intbv(0)[len(i.data):])
    state = Signal(intbv(0, min = 0 , max = 3))
    transferIn = Signal(False)
    transferOut = Signal(False)
    tValidOut = Signal(False)
    tReadyOut = Signal(False)

    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferIn.next = i.valid == 1 and tReadyOut == 1
        transferOut.next = tValidOut == 1 and o.ready == 1
        o.data.next = buf0

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == 0:
            tReadyOut.next = 1
        if transferIn and not transferOut:
            if state == 0:
                buf0.next = i.data
                state.next = 1
                tValidOut.next = 1
            if state == 1:
                buf1.next = i.data
                state.next = 2
                tReadyOut.next = 0

        if transferOut and not transferIn:
            if state == 1:
                state.next = 0
                tValidOut.next = 0
            if state == 2:
                state.next = 1
                buf0.next = buf1
                tReadyOut.next = 0

        if transferOut and transferIn:
            if state == 1:
                buf0.next = i.data
        
    return logic, out_reg
