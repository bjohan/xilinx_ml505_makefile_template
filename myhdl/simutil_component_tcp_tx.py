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
                try:
                    conn.send(bytes([i.data]))
                except BrokenPipeError as e:
                    raise StopSimulation(str(e))
            yield clk.posedge

    return logic
