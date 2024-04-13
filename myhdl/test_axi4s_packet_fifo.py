from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_packet_fifo import axi4s_packet_fifo

test_data =     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_last =     [0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    1]
test_delay_in = [1,    0,    0,    0,    0,    0,    3,    0,    0,    0,    0,    0]
test_delay_out =[1,    2,    3,    1,    0,    0,    3,    0,    0,    0,    0,    0]

test_data +=     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_last +=     [0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    1]
test_delay_in += [1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1]
test_delay_out +=[1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1]

test_data +=     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_last +=     [0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    1]
test_delay_in += [1,    1,    1,    1,    1,    1,    1,    0,    1,    1,    0,    0]
test_delay_out +=[1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1]

test_data +=     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_last +=     [0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    1]
test_delay_in += [1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1]
test_delay_out +=[1,    1,    1,    1,    1,    1,    0,    1,    1,    1,    0,    0]


@block
def test_axi4s_packet_fifo():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    i = Axi4sInterface(8); 
    o = Axi4sInterface(8);

    discard = Signal(False)
 
    axi4s_packet_fifo_inst = axi4s_packet_fifo(reset, clk, i, discard, o, 16)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(300):
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
    def gen_discard():
        yield i.last
        yield i.last
        yield clk.posedge
        yield clk.posedge
        #uncomment to test discard function
        #discard.next=True 
        yield clk.posedge
        yield clk.posedge
        discard.next=False

    @instance
    def read():
        yield reset.negedge
        yield tbReceiveSequence(clk, o, test_data, test_last, test_delay_out);
        raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data, test_last, test_delay_in);

    return clkgen, gen_reset, monitor, axi4s_packet_fifo_inst, gen_discard, write, read



tb = test_axi4s_packet_fifo();
tb.config_sim(trace=True)
tb.run_sim();
