from myhdl import *
from component_axi4s_prepender import axi4s_prepender
from interface_axi4s import Axi4sInterface

t_State = enum('S_POLL_THROUGH', 'S_POLL_MERGE', 'S_TRANSFER_THROUGH', 'S_TRANSFER_MERGE');
t_MuxState = enum('S_POLL', 'S_THROUGH', 'S_MERGE') 


@block
def axi4s_address_merge(reset, clk,
        through, merge, address, o):

    state = Signal(t_State.S_POLL_THROUGH) #main state
    muxState = Signal(t_MuxState.S_POLL) #control mux for main trasfers

    addressSignal = Signal(intbv(address)[len(o.data):])

    #internal signalfor input
    iReadyInt = Signal(True)

    prepended = Axi4sInterface(len(through.data))
    prepender_inst = axi4s_prepender(reset, clk, merge, prepended, addressSignal)

    @always_comb
    def bypass_transfer():
        if muxState == t_MuxState.S_POLL:
            through.ready.next = 0
            prepended.ready.next = 0
            o.valid.next = 0
            
        elif muxState == t_MuxState.S_THROUGH:
            through.ready.next = o.ready
            o.valid.next = through.valid
            o.data.next = through.data
            o.last.next = through.last

        elif muxState == t_MuxState.S_MERGE:
            prepended.ready.next = o.ready
            o.valid.next = prepended.valid
            o.data.next = prepended.data
            o.last.next = prepended.last

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_POLL_THROUGH:
            if through.valid:
                muxState.next = t_MuxState.S_THROUGH
                state.next = t_State.S_TRANSFER_THROUGH
            else:
                state.next = t_State.S_POLL_MERGE

        if state == t_State.S_POLL_MERGE:
            if prepended.valid:
                muxState.next = t_MuxState.S_MERGE
                state.next = t_State.S_TRANSFER_MERGE
            else:
                state.next = t_State.S_POLL_THROUGH

        if state == t_State.S_TRANSFER_THROUGH:
            if through.valid and o.ready and through.last:
                state.next = t_State.S_POLL_MERGE
                muxState.next = t_MuxState.S_POLL

        if state == t_State.S_TRANSFER_MERGE:
            if prepended.valid and o.ready and prepended.last:
                state.next = t_State.S_POLL_THROUGH
                muxState.next = t_MuxState.S_POLL

    return logic, bypass_transfer, prepender_inst
