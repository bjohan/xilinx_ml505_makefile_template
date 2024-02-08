from myhdl import *
import sys, select, termios, tty

class NonBlockingReader():
    def __init__(self):
        self.spoll = select.poll()
        self.spoll.register(sys.stdin, select.POLLIN)

    def read(self):
        if self.spoll.poll(0):
            ch = sys.stdin.read(1)
            return ch 
        return None

@block
def stdin_rx(reset, clk, o):
    transfer = Signal(False)
    rd = NonBlockingReader()

    @instance
    def logic():
        yield reset.negedge
        while True:
            if transfer == 0:
                d = rd.read()
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
