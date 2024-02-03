from myhdl import *
from component_dpbram import dpbram
@block
def dpbram_fifo(reset, clk, din, we, ready_o, dout, re, valid_o, depth):
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    raddr = Signal(modbv(0, min = 0 , max = depth))
    
    dout_a = Signal(intbv(0)[len(din):])
    wr_b = Signal(False)
    din_b = Signal(intbv(0)[len(din):])
    w = Signal(False)
    r = Signal(False)
    readDelay = Signal(False)
    valid = Signal(False)
    ready = Signal(False)
    dpbram_inst = dpbram(clk, w, waddr, din, dout_a, clk, wr_b, raddr, din_b, dout, depth)


    @always_comb
    def ready_empty():
        ready.next = waddrp1 != raddr
        ready_o.next = ready
        valid.next = waddr != raddr and not readDelay
        valid_o.next = valid
        w.next = we and ready;
        r.next = re and valid;

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if w:
            waddr.next = waddr+1
            waddrp1.next = waddrp1+1

        readDelay.next = 0
        if r:
            raddr.next = raddr+1
            readDelay.next = 1

    return logic, dpbram_inst, ready_empty

