from myhdl import *
import sys
@block
def tcp_tx(reset, clk, i, conn):
    @instance
    def logic():
        yield reset.negedge
        i.ready.next = 1
        while True:
            if i.valid and i.ready:
                conn.send(bytes([i.data]))
            yield clk.posedge

    return logic
