from myhdl import *
import sys
@block
def tcp_tx(reset, clk, i, conn):
    @instance
    def logic():
        buf =b''
        yield reset.negedge
        i.ready.next = 1
        while True:
            if i.valid and i.ready:
                buf+=bytes([i.data])
            if (not i.valid and len(buf)) or len(buf)>1024:
                try:
                    conn.send(buf)
                    buf=b''
                except BrokenPipeError as e:
                    raise StopSimulation(str(e))
            yield clk.posedge

    return logic
