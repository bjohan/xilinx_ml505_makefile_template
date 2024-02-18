from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_IDLE', 'S_PREPEND', 'S_TRANSFER');

@block
def axi4s_prepender(reset, clk, i, o, prep):
    ww = len(i.data)
    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_IDLE)

    transfer = Signal(False)
    num = Signal(intbv(0, min = 0, max = len(prep)/len(i.data)+1));
    intValidOut = Signal(False)
    tLastOut = Signal(False)
    prepData = Signal(modbv(0)[len(prep):])
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        o.last.next = tLastOut
        transferOut.next = tValidOut and o.ready

    @always_comb
    def bypass_transfer():
        if transfer:
            o.data.next = i.data;
            tValidOut.next = i.valid;
            tLastOut.next = i.last
            tReadyOut.next = o.ready;
            
        else:
            tReadyOut.next = 0
            o.data.next = prepData[ww:]
            tValidOut.next = intValidOut
            tLastOut.next = 0
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_IDLE:
            if i.valid == 1:
                prepData.next = prep
                intValidOut.next = 1
                state.next = t_State.S_PREPEND
                num.next = 0
                transfer.next = 0
        if state == t_State.S_PREPEND:
            if transferOut:
                prepData.next = prepData >> ww
                if num == len(prep)/len(i.data)-1:
                    state.next = t_State.S_TRANSFER
                    transfer.next = 1
                num.next = num+1
        if state == t_State.S_TRANSFER:
            if transferOut:
                if tLastOut:
                    state.next = t_State.S_IDLE
                    intValidOut.next = 0
                    transfer.next = 0
        
    return logic, out_reg, bypass_transfer
