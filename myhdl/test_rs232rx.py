from myhdl import *
from component_rs232tx import rs232tx
from component_rs232rx import rs232rx
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence


test_data =     [0xFF, 0xAA, 0x00, 0x01, 0x55, 0xFF, 0xF0, 0x0F]
test_last =     [0,    0,    0,    0,    0,    0,    0,    0]
test_delay_in = [0,    0,    1,    1,    0,    0,    3,    0]
test_delay_out =[1,    2,    3,    1,    0,    0,    3,    0]


@block
def test_rs232rx():
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    i = Axi4sInterface(8)
    o = Axi4sInterface(8)
    txd = Signal(True)
    rs232tx_inst = rs232tx(reset, clk, i, txd, 32)
    rs232rx_inst = rs232rx(reset, clk, o, txd, 32);

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
    def read():
        yield reset.negedge
        yield tbReceiveSequence(clk, o, test_data, test_last, test_delay_out);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data, test_last, test_delay_in);

    return clkgen, gen_reset, monitor, rs232tx_inst, rs232rx_inst, write, read

tb = test_rs232rx();
tb.config_sim(trace=True)
tb.run_sim();
