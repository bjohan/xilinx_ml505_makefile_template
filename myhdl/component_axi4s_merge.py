from myhdl import *
from component_axi4s_prepender import axi4s_prepender
from interface_axi4s import Axi4sInterface

t_State = enum('S_IDLE_POLL_A', 'S_IDLE_POLL_B', 'S_TRANSFER_A', 'S_TRANSFER_B');
t_MuxState = enum('S_IDLE', 'S_FROM_A', 'S_FROM_B') 


@block
def axi4s_merge(reset, clk, ia, ib, o):

    state = Signal(t_State.S_IDLE_POLL_A) #main state
    muxState = Signal(t_MuxState.S_IDLE) #control mux for main trasfers



    @always_comb
    def mux_logic():
        if muxState == t_MuxState.S_IDLE:
            ia.ready.next = 0
            ib.ready.next = 0
            o.valid.next = 0
            
        elif muxState == t_MuxState.S_FROM_A:
            ia.ready.next = o.ready
            o.valid.next = ia.valid
            o.data.next = ia.data
            o.last.next = ia.last

        elif muxState == t_MuxState.S_FROM_B:
            ib.ready.next = o.ready
            o.valid.next = ib.valid
            o.data.next = ib.data
            o.last.next = ib.last

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_IDLE_POLL_A:
            if ia.valid:
                muxState.next = t_MuxState.S_FROM_A
                state.next = t_State.S_TRANSFER_A
            else:
                state.next = t_State.S_IDLE_POLL_B

        if state == t_State.S_IDLE_POLL_B:
            if ib.valid:
                muxState.next = t_MuxState.S_FROM_B
                state.next = t_State.S_TRANSFER_B
            else:
                state.next = t_State.S_IDLE_POLL_A

        if state == t_State.S_TRANSFER_A:
            if ia.valid and o.ready and ia.last:
                state.next = t_State.S_IDLE_POLL_B
                muxState.next = t_MuxState.S_IDLE

        if state == t_State.S_TRANSFER_B:
            if ib.valid and o.ready and ib.last:
                state.next = t_State.S_IDLE_POLL_A
                muxState.next = t_MuxState.S_IDLE

    return logic, mux_logic
