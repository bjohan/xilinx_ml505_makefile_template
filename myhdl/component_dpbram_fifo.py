from myhdl import *
from component_dpbram import dpbram
@block
def dpbram_fifo(reset, clk, din, we, ready_o, dout, re, valid_o, empty_o, newData, depth):
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    raddr = Signal(modbv(0, min = 0 , max = depth))
    raddrp1 = Signal(modbv(1, min = 0 , max = depth))
   
    dout_a = Signal(intbv(0)[len(din):])
    wr_b = Signal(False)
    din_b = Signal(intbv(0)[len(din):])
    w = Signal(False)
    r = Signal(False)
    readDelay = Signal(False)
    valid = Signal(False)
    empty = Signal(False)
    emptyAfterRead = Signal(False)
    ready = Signal(False)
    newR = Signal(False)
    dpbram_inst = dpbram(clk, w, waddr, din, dout_a, clk, wr_b, raddr, din_b, dout, depth)


    @always_comb
    def ready_empty():
        ready.next = waddrp1 != raddr
        ready_o.next = ready
        empty.next = waddr == raddr;
        emptyAfterRead.next = waddr==raddrp1
        empty_o.next = empty
        valid_o.next = not empty
        w.next = we and ready;
        r.next = re and not empty;

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            newR.next = ((not empty) and re and not emptyAfterRead) or (empty and we)
            newData.next = newR
            #valid_o.next = 0
            if w:
                waddr.next = waddr+1
                waddrp1.next = waddrp1+1
                #if empty:
                    #valid_o.next = 1

            #readDelay.next = 0
            if r:
                raddr.next = raddr+1
                raddrp1.next = raddrp1+1
                #valid_o.next = 1
                #readDelay.next = 1
            #valid.next = readDelay

    return logic, dpbram_inst, ready_empty

