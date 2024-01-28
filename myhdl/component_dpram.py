from myhdl import *

@block
def dpram(reset, clk, din, waddr, dout, raddr, we, depth):
    mem = [Signal(intbv(0)[len(din):]) for i in range(depth)]

    @always(clk.posedge)
    def write():
        if we:
            mem[waddr].next = din

    @always_comb
    def read():
        dout.next = mem[raddr]

    return write, read

