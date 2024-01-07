from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'ESCAPE');

@block
def escaper(reset, clk, 
        tDataIn, tValidIn, tReadyOut_o, tLastIn,
        tDataOut, tValidOut_o, tReadyIn, tLastOut,
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
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferIn.next = tValidOut and tReadyOut
        transferOut.next = tValidOut and tReadyIn

    @always_comb
    def bypass_transfer():
        if transfer:
            tDataOut.next = tDataIn;
            tValidOut.next = tValidIn;
            tReadyOut.next = tReadyIn;
            if tDataIn != escapeCode:
                tLastOut.next = tLastIn
            
        else:
            tReadyOut.next = 0
            tDataOut.next = escapeCode;
            tLastOut.next = tLastBuf;
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            transfer.next = 1
            if transferIn:
                if tDataIn == escapeCode:
                    state.next = t_State.ESCAPE
                    transfer.next = 0
                    tLastBuf.next = tLastIn
        elif state == t_State.ESCAPE:
            if transferOut:
                state.next = t_State.S_TRANSFER
                transfer.next = 1
        
    return logic, out_reg, bypass_transfer
