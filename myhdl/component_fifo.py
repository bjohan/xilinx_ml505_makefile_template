from myhdl import *
from component_dpram import dpram
@block
def fifo(reset, clk, din, we, ready_o, dout, re, valid_o, depth):
    waddr = Signal(modbv(0, min = 0 , max = depth))
    waddrp1 = Signal(modbv(1, min = 0 , max = depth))
    raddr = Signal(modbv(0, min = 0 , max = depth))
    #wint = Signal(False)
    #dwint = Signal(intbv(0)[len(din):])
    #waddrint = Signal(modbv(0, min = 0, max = depth))
    #dpram_inst = dpram(reset, clk, dwint, waddrint, dout, raddr, wint, depth)
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
        #if modbv(waddr+1,min=0, max=depth) == raddr:
        #    ready.next = 1
        #else:
        #    ready.next = 0

        #if raddr == waddr:
        #    valid.next = 0
        #else:
        #    valid.next = 1

        if w:
            waddr.next = waddr+1
            waddrp1.next = waddrp1+1

        if r:
            raddr.next = raddr+1

        #if we:
        #    #print(modbv(waddr+1, min = 0, max = depth),raddr)
        #    if modbv(waddr+1, min = 0 , max = depth) != raddr:
        #        waddr.next = waddr+1
        #        waddrint.next = waddr+1;
        #        dwint.next = din
        #        wint.next = 1
        #        if modbv(waddr+2, min = 0 , max=depth) == raddr:
        #            ready.next = 1
        #        else:
        #            ready.next = 0
        #    else:
        #        wint.next = 0
        #else:
        #    wint.next = 0
        #if re:
        #    if waddr != raddr:
        #        raddr.next = raddr+1
        #    if modbv(raddr+1, min = 0, max = depth) == waddr:
        #            valid.next = 0

    return logic, dpram_inst, ready_empty

