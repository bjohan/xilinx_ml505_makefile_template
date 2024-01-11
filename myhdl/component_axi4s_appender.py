from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_APPEND');

@block
def axi4s_appender(reset, clk, 
        tDataIn, tValidIn, tReadyOut_o, tLastIn,
        tDataOut, tValidOut_o, tReadyIn, tLastOut,
        app):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    transfer = Signal(True)
    num = Signal(intbv(0, min = 0, max = len(app)/len(tDataIn)+1));
    tValidInt = Signal(False)

    numWords = Signal(intbv(int(len(app)/len(tDataIn)))[8:])
    isLast = Signal(False)
 
    @always_comb
    def out_reg():
        tValidOut_o.next = tValidOut
        tReadyOut_o.next = tReadyOut
        transferOut.next = tValidOut and tReadyIn
        isLast.next = ((num+1) == numWords)

    @always_comb
    def bypass_transfer():
        if transfer:
            tDataOut.next = tDataIn;
            tValidOut.next = tValidIn;
            tLastOut.next = 0
            tReadyOut.next = tReadyIn;
            
        else:
            tReadyOut.next = 0
            tDataOut.next = app[(num+1)*len(tDataIn):num*len(tDataIn)]
            tValidOut.next = tValidInt
            tLastOut.next = isLast
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            transfer.next = 1
            num.next = 0
            if transferOut and tLastIn:
                    state.next = t_State.S_APPEND
                    transfer.next = 0
                    tValidInt.next = 1
        if state == t_State.S_APPEND:
            if transferOut:
                if isLast:
                    state.next = t_State.S_TRANSFER
                    transfer.next = 1
                    tValidInt.next = 0
                num.next = num+1
        
    return logic, out_reg, bypass_transfer
