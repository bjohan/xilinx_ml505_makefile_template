from myhdl import *

@block
def ram(reset, clk, din, dout, addr, we, depth):
    mem = [Signal(intbv(0)[len(din):]) for i in range(depth)]

    @always(clk.posedge)
    def write():
        if we:
            mem[addr].next = din

    @always_comb
    def read():
        dout.next = mem[addr]

    return write, read

