from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_IDLE', 'S_PREPEND', 'S_TRANSFER');

@block
def axi4s_prepender(reset, clk, 
        tDataIn, tValidIn, tReadyOut_o, tLastIn,
        tDataOut, tValidOut_o, tReadyIn, tLastOut_o,
        prep):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_IDLE)

    transfer = Signal(False)
    num = Signal(intbv(0, min = 0, max = len(prep)/len(tDataIn)+1));
    tValidInt = Signal(False)
    tLastOut = Signal(False)
 
    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        tLastOut_o.next = tLastOut
        transferOut.next = tValidOut and tReadyIn

    @always_comb
    def bypass_transfer():
        if transfer:
            tDataOut.next = tDataIn;
            tValidOut.next = tValidIn;
            tLastOut.next = tLastIn
            tReadyOut.next = tReadyIn;
            
        else:
            tReadyOut.next = 0
            tDataOut.next = prep[(num+1)*len(tDataIn):num*len(tDataIn)]
            tValidOut.next = tValidInt
            tLastOut.next = 0
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_IDLE:
            if tValidIn == 1:
                tValidInt.next = 1
                state.next = t_State.S_PREPEND
                num.next = 0
                transfer.next = 0
        if state == t_State.S_PREPEND:
            if transferOut:
                if num == len(prep)/len(tDataIn)-1:
                    state.next = t_State.S_TRANSFER
                    transfer.next = 1
                num.next = num+1
        if state == t_State.S_TRANSFER:
            if transferOut:
                if tLastOut:
                    state.next = t_State.S_IDLE
                    tValidInt.next = 0
                    transfer.next = 0
        
    return logic, out_reg, bypass_transfer
