from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'ESCAPE');

@block
def escaper(reset, clk, i, o, 
        escapeCode):

    
    tReadyOut = Signal(True)
    tValidOut = Signal(False)
    transferIn = Signal(False)
    transferOut = Signal(False)
    tLastBuf = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    transfer = Signal(False)
    
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferIn.next = i.valid and tReadyOut
        transferOut.next = tValidOut and o.ready

    @always_comb
    def bypass_transfer():
        if transfer:
            o.data.next = i.data;
            tValidOut.next = i.valid;
            tReadyOut.next = o.ready;
            if i.data != escapeCode:
                o.last.next = i.last
            
        else:
            tReadyOut.next = 0
            o.data.next = escapeCode;
            o.last.next = tLastBuf;
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            transfer.next = 1
            if transferIn:
                if i.data == escapeCode:
                    state.next = t_State.ESCAPE
                    transfer.next = 0
                    tLastBuf.next = i.last
        elif state == t_State.ESCAPE:
            if transferOut:
                state.next = t_State.S_TRANSFER
                transfer.next = 1
        
    return logic, out_reg, bypass_transfer
