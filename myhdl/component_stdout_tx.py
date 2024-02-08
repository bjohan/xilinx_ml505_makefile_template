from myhdl import *
import sys
@block
def stdout_tx(reset, clk, i):
    @instance
    def logic():
        yield reset.negedge
        i.ready.next = 1
        while True:
            if i.valid and i.ready:
                sys.stdout.write(chr(i.data))
            yield clk.posedge

    return logic
