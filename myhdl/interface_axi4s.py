from myhdl import *

class Axi4sInterface:
    def __init__(self, bits, withLast = True):
        self.data = Signal(intbv(0xAA)[bits:])
        self.valid = Signal(False)
        self.ready = Signal(False)
        if withLast:
            self.last = Signal(False)

    def transacts(self):
        return (self.ready == 1)  and (self.valid == 1)
