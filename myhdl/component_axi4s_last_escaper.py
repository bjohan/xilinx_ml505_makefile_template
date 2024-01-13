from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_ESCAPE', 'S_ESC_LAST', 'S_END_LAST', 'S_ESCAPE_TRANSFER_LAST','S_TRANSFER_LAST');

@block
def axi4s_last_escaper(reset, clk, 
        tDataIn, tValidIn, tReadyOut_o, tLastIn,
        tDataOut_o, tValidOut_o, tReadyIn,
        esc, end):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    transfer = Signal(True)
    tValidInt = Signal(False)
    tDataOutInt = Signal(intbv(0)[len(tDataIn):])
    tDataOut = Signal(intbv(0)[len(tDataIn):])
    
 
    @always_comb
    def out_reg():
        tDataOut_o.next = tDataOut
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferOut.next = tValidOut and tReadyIn

    @always_comb
    def bypass_transfer():
        if (transfer and not tLastIn) or (state == t_State.S_TRANSFER_LAST):
            tDataOut.next = tDataIn;
            tValidOut.next = tValidIn;
            tReadyOut.next = tReadyIn;
        elif transfer and tLastIn:
            tReadyOut.next = 0
            tValidOut.next = 0
            
        else:
            tReadyOut.next = 0
            tDataOut.next = tDataOutInt
            tValidOut.next = tValidInt
        

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_TRANSFER:
            transfer.next = 1
            if transferOut:
                if tDataOut == esc:
                    state.next = t_State.S_ESCAPE
                    transfer.next = 0
                    tValidInt.next = 1
                    tDataOutInt.next = esc
            if tLastIn and tValidIn:
                state.next = t_State.S_ESC_LAST;
                transfer.next = 0
                tDataOutInt.next = esc;
                tValidInt.next = 1
                
        if state == t_State.S_ESCAPE:
            if transferOut:
                state.next = t_State.S_TRANSFER
                transfer.next = 1
                tValidInt.next = 0

        if state == t_State.S_ESC_LAST:
            if transferOut:
                state.next = t_State.S_END_LAST
                tDataOutInt.next = end

        if state == t_State.S_END_LAST:
            if transferOut:
                    if tDataIn == esc:
                        tDataOutInt.next = esc
                        state.next = t_State.S_ESCAPE_TRANSFER_LAST
                    else:
                        state.next = t_State.S_TRANSFER_LAST
                        transfer.next = 1
       
        if state == t_State.S_ESCAPE_TRANSFER_LAST:
            if transferOut:
                state.next = t_State.S_TRANSFER_LAST
                transfer.next = 1
 
        if state == t_State.S_TRANSFER_LAST:
            if transferOut:
                state.next = t_State.S_TRANSFER
                tValidInt.next = 0
                
            
        
    return logic, out_reg, bypass_transfer
