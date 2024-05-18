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


def tbTransmit(clk, bus, data, last, delay):
    bus.valid.next = 0
    bus.data.next = data
    bus.last.next = last
    for d in range(delay):
        yield clk.posedge
    bus.valid.next = 1
    yield clk.posedge
    while not bus.ready:
        yield clk.posedge
    bus.valid.next = 0
    bus.last.next = 0

def tbTransmitSequence(clk, bus, dataSeq, lastSeq, delaySeq):
    for data, last, delay in zip(dataSeq, lastSeq, delaySeq):
        yield tbTransmit(clk, bus, data, last, delay)

def tbReceive(clk, bus, data, last, delay):
    for d in range(delay):
        yield clk.posedge
    bus.ready.next = 1
    yield clk.posedge
    while not bus.valid:
        yield clk.posedge
    if data != bus.data:
        print("Data does not match. Got", hex(bus.data), " expected ", hex(data))
        yield clk.posedge
        quit(-1)
    if last != bus.last:
        print("Last bit does not match when transfering", data, ". Got", bus.last, "expected", last)
        quit(-1)
    bus.ready.next = 0

def tbReceiveSequence(clk, bus, dataSeq, lastSeq, delaySeq):
    for data, last, delay in zip(dataSeq, lastSeq, delaySeq):
        yield tbReceive(clk, bus, data, last, delay)
