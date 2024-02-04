from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4sn import axi4sn


test_data_in = [0xA3A2A1A0, 0xB3B2B1B0, 0xC3C2C1C0]
test_delay_in= [0,          0,          1]
test_last_in = [0,          1,          1]

test_data_out = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_delay_out =[1,    2,    3,    1,    0,    0,    3,    0,    0,    0,    0,    0]
test_last_out = [0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    1]


@block
def test_axi4sn():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    i = Axi4sInterface(32)
    o = Axi4sInterface(8)
    axi4sn_inst = axi4sn(reset, clk, i, o, 4)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(100):
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
        yield tbReceiveSequence(clk, o, test_data_out, test_last_out, test_delay_out);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data_in, test_last_in, test_delay_in);


    return clkgen, gen_reset, monitor, axi4sn_inst, write, read

tb = test_axi4sn();
tb.config_sim(trace=True)
tb.run_sim();
