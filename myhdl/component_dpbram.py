from myhdl import *

@block
def dpbram(clk_a, wr_a, addr_a, din_a, dout_a, clk_b, wr_b, addr_b, din_b, dout_b, size):
    mem = [Signal(intbv(0)[len(din_a):]) for i in range(size)]

    @always(clk_a.posedge)
    def dpram_a():
        if wr_a:
            mem[addr_a].next = din_a
        dout_a.next = mem[addr_a]

    @always(clk_b.posedge)
    def dpram_b():
        if wr_b:
            mem[addr_b].next = din_b
        dout_b.next = mem[addr_b]


    return dpram_a, dpram_b

