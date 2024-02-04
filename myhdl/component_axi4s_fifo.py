from myhdl import *

from interface_axi4s import Axi4sInterface
from component_dpbram_fifo import dpbram_fifo
from component_axi4s_skidbuf import axi4s_skidbuf

t_State = enum('S_READ', 'S_WAIT', 'S_TRANSFER_DIRECT', 'S_TRANSFER_WAIT');

@block
def axi4s_fifo(reset, clk, i, o, depth):
    fifo_din = Signal(intbv(0)[len(i.data)+1:])
    fifo_dout = Signal(intbv(0)[len(i.data)+1:])

    state = Signal(t_State.S_READ)
    u = Axi4sInterface(len(i.data))
    empty = Signal(False)
    fifo_read = Signal(False)
    fifo_valid = Signal(False)
    i_fifo = dpbram_fifo(reset, clk, fifo_din, i.valid, i.ready, fifo_dout, fifo_read, fifo_valid, empty, depth) 
    i_skidbuf = axi4s_skidbuf(reset, clk,  u, o)

    @always_comb
    def out_reg():
        fifo_din.next[len(i.data)] = i.last
        fifo_din.next[len(i.data):0] = i.data
        u.data.next = fifo_dout[len(u.data):0]
        u.last.next = fifo_dout[len(u.data)] 
        
    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_READ:
            u.valid.next = 0
            fifo_read.next = 0
            if fifo_valid and u.ready:
                state.next = t_State.S_TRANSFER_DIRECT
                u.valid.next = 1
                fifo_read.next = 1
            if fifo_valid and not u.ready:
                state.next = t_State.S_TRANSFER_WAIT
                u.valid.next = 1
                fifo_read.next = 0

        if state == t_State.S_TRANSFER_DIRECT:
            u.valid.next = 0
            fifo_read.next = 0
            state.next = t_State.S_READ
            
        if state == t_State.S_TRANSFER_WAIT:
            if u.ready:
                u.valid.next = 0
                fifo_read.next = 1
                state.next = t_State.S_READ
             
                
        
    return logic, out_reg, i_fifo, i_skidbuf
