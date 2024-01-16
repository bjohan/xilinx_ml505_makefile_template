from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_CONSUME_ESCAPE', 'S_EXAMINE', 'S_TRANSFER_ESC');

@block
def axi4s_last_deescaper(reset, clk, 
        i, o, frameError, esc, end):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    transferIn = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    transfer = Signal(True)
    tValidInt = Signal(False)
    tDataOutInt = Signal(intbv(0)[len(i.data):])
    tDataOut = Signal(intbv(0)[len(i.data):])
    tReadyOutInt = Signal(False)
    
    nextIsLast = Signal(False)
    isEscape = Signal(False)
 
    @always_comb
    def out_reg():
        o.data.next = tDataOut
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferOut.next = tValidOut and o.ready
        transferIn.next = i.valid and tReadyOut

    @always_comb
    def bypass_transfer():
        isEscape.next = (i.data == esc)
        if transfer:
            tDataOut.next = i.data;
            tValidOut.next = i.valid and not isEscape;
            tReadyOut.next = o.ready and not isEscape;
            o.last.next = nextIsLast
        else:
            tDataOut.next = tDataOutInt
            tValidOut.next = tValidInt
            tReadyOut.next = tReadyOutInt
            o.last.next = nextIsLast
        

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_TRANSFER:
            transfer.next = 1
            frameError.next = 0
            if transferOut:
                nextIsLast.next = 0
            if isEscape and i.valid :
                state.next = t_State.S_CONSUME_ESCAPE
                transfer.next = 0
                tReadyOutInt.next = 1

        if state == t_State.S_CONSUME_ESCAPE:
            if transferIn:
                state.next = t_State.S_EXAMINE
                transfer.next = 0
                tValidInt.next = 0
                tReadyOutInt.next = 1

        if state == t_State.S_EXAMINE:
            if transferIn:
                if i.data == esc:
                    state.next = t_State.S_TRANSFER_ESC
                    tReadyOutInt.next = 0
                    tDataOutInt.next = esc;
                    tValidInt.next = 1
                elif i.data == end:
                    nextIsLast.next = 1
                    transfer.next = 1
                    state.next = t_State.S_TRANSFER
                else:
                    frameError.next = 1;
                    transfer.next = 1
                    state.next = t_State.S_TRANSFER
                    

        if state == t_State.S_TRANSFER_ESC:
               if transferOut == 1:
                    transfer.next =1 
                    tValidInt.next =0
                    nextIsLast.next = 0
                    state.next = t_State.S_TRANSFER
            

        
    return logic, out_reg, bypass_transfer
