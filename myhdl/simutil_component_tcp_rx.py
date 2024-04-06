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
                    if not conn.connectionValid():
                        raise StopSimulation("TCP connection no longer valid")
                    d = conn.recv(1)
                    if d is not None and len(d):
                        transfer.next = 1
                        o.valid.next = 1
                        o.data.next = ord(d)
                except ConnectionResetError as e:
                    raise StopSimulation(str(e))
                except TimeoutError:
                    #print("timeout")
                    pass
                except BlockingIOError as e:
                    #print("block", str(e))
                    pass
                yield clk.posedge
            else:
                if o.ready == True:
                    o.valid.next = 0
                    transfer.next = 0
                yield clk.posedge
    return logic
