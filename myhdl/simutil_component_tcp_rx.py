from myhdl import *
import sys, select, termios, tty

@block
def tcp_rx(reset, clk, o, conn):
    transfer = Signal(False)

    @instance
    def logic():
        yield reset.negedge
        while True:
            if transfer == 0:
                try:
                    d = conn.recv(1)
                except ConnectionResetError as e:
                    raise StopSimulation(str(e))
                if d is not None and len(d):
                    transfer.next = 1
                    o.valid.next = 1
                    o.data.next = ord(d)
                yield clk.posedge
            else:
                while transfer:
                    if o.ready:
                        o.valid.next = 0
                        transfer.next = 0
                    yield clk.posedge
    return logic
