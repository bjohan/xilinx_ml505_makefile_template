from myhdl import *

t_State = enum('S_FIRST', 'S_MUX_TRANSFER', 'S_BYPASS_TRANSFER', 'S_INT_TO_MUX', 'S_INT_TO_BYPASS', 'S_BROADCAST');
t_MuxState = enum('S_INTERNAL', 'S_BYPASS', 'S_MUX') 


@block
def axi4s_address_switch(reset, clk,
        i, om, address, o):

    state = Signal(t_State.S_FIRST) #main state
    returnState = Signal(t_State.S_BYPASS_TRANSFER) #return state for after specific transfers
    
    muxState = Signal(t_MuxState.S_INTERNAL) #control mux for main trasfers
    

    #internal signalfor input
    iReadyInt = Signal(True)

    #internal registers for bypass 
    oValidInt = Signal(False)
    oDataInt = Signal(intbv(0)[len(o.data):])
    oLastInt = Signal(False)

    #internal registers for muxed transfers
    omValidInt = Signal(False)
    omDataInt = Signal(intbv(0)[len(o.data):])
    omLastInt = Signal(False)

    #State variables for broadcast mechanism
    broadcastBufData = Signal(intbv(0)[len(o.data):])
    broadcastBufLast = Signal(intbv(0)[len(o.data):])
    broadcastBufValid = Signal(False)
    broadcastByp = Signal(False)
    broadcastMux = Signal(False)

    @always_comb
    def bypass_transfer():
        if muxState == t_MuxState.S_INTERNAL:
            i.ready.next = iReadyInt
            o.data.next = oDataInt
            o.valid.next = oValidInt
            o.last.next = oLastInt
            om.data.next = omDataInt
            om.valid.next = omValidInt
            om.last.next = omLastInt
            
        elif muxState == t_MuxState.S_BYPASS:
            i.ready.next = o.ready
            o.valid.next = i.valid
            o.data.next = i.data
            o.last.next = i.last
            om.valid.next = 0

        elif muxState == t_MuxState.S_MUX:
            i.ready.next = om.ready
            om.valid.next = i.valid
            om.data.next = i.data
            om.last.next = i.last
            o.valid.next = 0

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_FIRST:
            muxState.next = t_MuxState.S_INTERNAL
            if i.valid == 1:
                iReadyInt.next = 0
                if i.data == address:
                    state.next= t_State.S_MUX_TRANSFER
                    muxState.next = t_MuxState.S_MUX
                elif i.data == i.data.max-1:
                    #oDataInt.next = i.data
                    #omDataInt.next = i.data
                    #oLastInt.next = i.last;
                    #omLastInt.next = i.last
                    broadcastBufData.next = i.data
                    broadcastBufLast.next = i.last
                    broadcastBufValid.next = 1
                    broadcastByp.next = 0
                    broadcastMux.next = 0
                    state.next = t_State.S_BROADCAST
                else:
                    oDataInt.next = i.data
                    returnState.next = t_State.S_BYPASS_TRANSFER
                    state.next = t_State.S_INT_TO_BYPASS
                    oValidInt.next = 1
                    oLastInt.next = i.last
                    #muxState.next = t_MuxState.S_BYPASS_TRANSFER
    
        if state == t_State.S_MUX_TRANSFER:
            if i.valid and om.ready and i.last:
                state.next = t_State.S_FIRST
                muxState.next = t_MuxState.S_INTERNAL
                omValidInt.next = 0
                iReadyInt.next = 1

        if state == t_State.S_BYPASS_TRANSFER:
            if i.valid and o.ready and i.last:
                state.next = t_State.S_FIRST
                muxState.next = t_MuxState.S_INTERNAL
                oValidInt.next = 0
                iReadyInt.next = 1

        if state == t_State.S_INT_TO_BYPASS:
            if o.ready: #muxState, oValidInt and oDataInt must be set when entering this state
                state.next = returnState;
                if returnState == t_State.S_BYPASS_TRANSFER:
                    muxState.next = t_MuxState.S_BYPASS
                    iReadyInt.next = 1
                if oLastInt:
                    oValidInt.next = 0
                    iReadyInt.next = 1
                    state.next = t_State.S_FIRST
        
        if state == t_State.S_INT_TO_MUX:
            if om.ready: #muxState, omValidInt and omDataInt must be set when entering this state
                state.next = returnState;
                if returnState == t_State.S_MUX_TRANSFER:
                    muxState.next = t_MuxState.S_MUX
                    iReadyInt.next = 1
        
    
        if state == t_State.S_BROADCAST:
            if not broadcastBufValid:
                iReadyInt.next = 1
                if i.valid and iReadyInt:
                    broadcastBufValid.next = 1
                    broadcastBufData.next = i.data
                    broadcastBufLast.next = i.last
                    iReadyInt.next = 0
            else:
                if not broadcastByp:
                    oDataInt.next = broadcastBufData
                    oLastInt.next = broadcastBufLast
                    oValidInt.next = 1
                    if oValidInt and o.ready:
                        oValidInt.next = 0
                        broadcastByp.next = 1
                if not broadcastMux:
                    omDataInt.next = broadcastBufData
                    omLastInt.next = broadcastBufLast
                    omValidInt.next = 1
                    if omValidInt and om.ready:
                        omValidInt.next = 0
                        broadcastMux.next = 1
            if broadcastMux and broadcastByp: #transfered both bypass and mux
                if broadcastBufLast:
                    state.next = t_State.S_FIRST
                    iReadyInt.next = 1
                broadcastBufValid.next = 0
                broadcastByp.next = 0
                broadcastMux.next = 0
                

    return logic, bypass_transfer
