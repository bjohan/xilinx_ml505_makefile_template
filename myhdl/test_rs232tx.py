from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence

from component_rs232tx import rs232tx

test_data =     [0xFF, 0xAA, 0x00, 0x01, 0x55, 0xFF, 0xF0, 0x0F]
test_last =     [0,    0,    0,    0,    0,    0,    0,    0]
test_delay_in = [0,    0,    1,    1,    0,    0,    3,    0]

@block
def test_rs232tx():
    reset = ResetSignal(0, active=1, isasync=False)
    clk = Signal(False)
    i = Axi4sInterface(8)
    txd = Signal(False)

    rs232tx_inst = rs232tx(reset, clk, i, txd, 5)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def monitor():
        for i in range(10000):
            yield clk.posedge
        print("Simulation did not end successfully")
        quit(-1)

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data, test_last, test_delay_in);
        if not i.ready:
            yield i.ready.posedge
        yield clk.posedge
        raise StopSimulation("Simulation ended successfully")

    return clkgen, gen_reset, monitor, rs232tx_inst, write

tb = test_rs232tx();
tb.config_sim(trace=True)
tb.run_sim();
