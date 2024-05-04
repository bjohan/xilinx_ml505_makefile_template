from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_APPEND');

@block
def axi4s_appender(reset, clk, i, o, 
        app):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    transfer = Signal(True)
    num = Signal(intbv(0, min = 0, max = len(app)/len(i.data)+1));
    ivalidt = Signal(False)

    numWords = Signal(intbv(int(len(app)/len(i.data)))[8:])
    isLast = Signal(False)
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferOut.next = tValidOut and o.ready
        isLast.next = ((num+1) == numWords)

    @always_comb
    def bypass_transfer():
        if transfer:
            o.data.next = i.data;
            tValidOut.next = i.valid;
            o.last.next = 0
            tReadyOut.next = o.ready;
            
        else:
            tReadyOut.next = 0
            o.data.next = app[(num+1)*len(i.data):num*len(i.data)]
            tValidOut.next = ivalidt
            o.last.next = isLast
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            transfer.next = 1
            num.next = 0
            if transferOut and i.last:
                    state.next = t_State.S_APPEND
                    transfer.next = 0
                    ivalidt.next = 1
        if state == t_State.S_APPEND:
            if transferOut:
                if isLast:
                    state.next = t_State.S_TRANSFER
                    transfer.next = 1
                    ivalidt.next = 0
                num.next = num+1
        
    return logic, out_reg, bypass_transfer
