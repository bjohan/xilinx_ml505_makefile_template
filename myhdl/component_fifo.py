from myhdl import *
from component_dpram import dpram
@block
def fifo(reset, clk, din, we, ready_o, dout, re, valid_o, depth):
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    raddr = Signal(modbv(0, min = 0 , max = depth))
    w = Signal(False)
    r = Signal(False)
    valid = Signal(False)
    ready = Signal(False)
    dpram_inst = dpram(reset, clk, din,waddr, dout, raddr, w, depth)


    @always_comb
    def ready_empty():
        ready.next = waddrp1 != raddr
        ready_o.next = ready
        valid.next = waddr != raddr
        valid_o.next = valid
        w.next = we and ready;
        r.next = re and valid;

    @always_seq(clk.posedge, reset=reset)
    def logic():

        if w:
            waddr.next = waddr+1
            waddrp1.next = waddrp1+1

        if r:
            raddr.next = raddr+1


    return logic, dpram_inst, ready_empty

