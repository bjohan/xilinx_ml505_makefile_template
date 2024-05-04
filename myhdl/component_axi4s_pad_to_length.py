from myhdl import *
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_TRANSFER', 'S_APPEND');

@block
def axi4s_pad_to_length(reset, clk, i, o, minimum_length, pad):

    tReadyOut = Signal(False)
    tValidOut = Signal(False)
    transferOut = Signal(False)
    state = Signal(t_State.S_TRANSFER)

    nTransfered = Signal(modbv(0)[32:])    
    numPad = Signal(modbv(0)[32:])    

    transfer = Signal(True)
    transferLast = Signal(False)

    num = Signal(modbv(0)[32:])
    ivalidt = Signal(False)

    isLast = Signal(False)
    needsPadding = Signal(False)
 
    @always_comb
    def out_reg():
        o.valid.next = tValidOut
        i.ready.next = tReadyOut
        transferOut.next = tValidOut and o.ready
        isLast.next = ((num+1) == numPad)
        needsPadding.next = i.last and (nTransfered+1) < minimum_length 

    @always_comb
    def bypass_transfer():
        if needsPadding:
            o.last.next = 0
        else:
            o.last.next = i.last

        if transfer:
            o.data.next = i.data;
            tValidOut.next = i.valid;
            tReadyOut.next = o.ready;
            
        else:
            tReadyOut.next = 0
            o.data.next = pad
            tValidOut.next = ivalidt
            o.last.next = isLast
        

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_TRANSFER:
            transfer.next = 1
            num.next = 0
            if transferOut:
                nTransfered.next = nTransfered + 1
                if i.last:
                    if needsPadding:
                        state.next = t_State.S_APPEND
                        transfer.next = 0
                        ivalidt.next = 1
                        if nTransfered >= (minimum_length - 1):
                            numPad.next = 0
                        else:
                            numPad.next = minimum_length - nTransfered - 1
                    nTransfered.next = 0
        if state == t_State.S_APPEND:
            if transferOut:
                if isLast:
                    state.next = t_State.S_TRANSFER
                    transfer.next = 1
                    ivalidt.next = 0
                num.next = num+1
        
    return logic, out_reg, bypass_transfer
