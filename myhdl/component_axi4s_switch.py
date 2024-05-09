from myhdl import *

t_State = enum('S_IDLE', 'S_TO_A', 'S_TO_B');


@block
def axi4s_switch(reset, clk, i, oa, ob, toA, toB):

    state = Signal(t_State.S_IDLE) #main state
    
    @always_comb
    def mux_transfer():
        if state == t_State.S_IDLE:
            i.ready.next = 0
            ob.valid.next = 0
            oa.valid.next = 0
            
        elif state == t_State.S_TO_A:
            i.ready.next = oa.ready
            oa.valid.next = i.valid
            oa.data.next = i.data
            oa.last.next = i.last
            ob.valid.next = 0

        elif state == t_State.S_TO_B:
            i.ready.next = ob.ready
            ob.valid.next = i.valid
            ob.data.next = i.data
            ob.last.next = i.last
            oa.valid.next = 0

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if state == t_State.S_IDLE:
            if i.valid and toA and not toB:
                state.next = t_State.S_TO_A
            if i.valid and toB and not toA:
                state.next = t_State.S_TO_B

        elif state == t_State.S_TO_A:
            if i.valid and oa.ready and i.last:
                state.next = t_State.S_IDLE
        elif state == t_State.S_TO_B:
            if i.valid and ob.ready and i.last:
                state.next = t_State.S_IDLE
        
    return logic, mux_transfer
