from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_TRUNCATE');

@block
def axi4s_truncate_to_length(reset, clk, i, o, maximum_length):

    tValidOut = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    nTransfered = Signal(modbv(0)[32:])    

    needsTruncating = Signal(False)
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        needsTruncating.next = ((nTransfered+1) == maximum_length) and not i.last

    @always_comb
    def bypass_transfer():
        if needsTruncating:
            o.last.next = 1
        else:
            o.last.next = i.last

        if state == t_State.S_TRANSFER:
            o.data.next = i.data;
            tValidOut.next = i.valid;
            i.ready.next = o.ready
            o.last.next = i.last or needsTruncating;
            
        else:
            i.ready.next = 1
            tValidOut.next = 0
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            if tValidOut and o.ready:
                nTransfered.next = nTransfered + 1
                if needsTruncating:
                    state.next = t_State.S_TRUNCATE
                    nTransfered.next = 0
                if i.last:
                    nTransfered.next = 0
        if state == t_State.S_TRUNCATE:
            if i.valid:
                if i.last:
                    state.next = t_State.S_TRANSFER
        
    return logic, out_reg, bypass_transfer
