from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_rs232tx import rs232tx
from component_rs232rx import rs232rx
from component_axi4s_last_deescaper import axi4s_last_deescaper
from component_axi4s_last_escaper import axi4s_last_escaper
from component_axi4s_fifo import axi4s_fifo
from component_axi4s_skidbuf import axi4s_skidbuf
from component_application_test_str import application_test_str
test_data_in = [0xc0, 0x3, 0xFF]
test_delay_in= [0,   0,   1]
test_last_in = [0,   1,   1]

test_data_out = test_data_in
#test_data_out = [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3]
test_delay_out =[1,   2,   3]
test_last_out = [0,   0,   0]



@block
def simulation_serial_and_escaping():

    baudDiv = 100
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    ser_in = Signal(True)
    ser_out = Signal(True)
    frameError = Signal(False)


    mdio_in = Signal(False)
    mdio_out = Signal(False)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)

    i = Axi4sInterface(8)
    toskid = Axi4sInterface(8)
    todeesc = Axi4sInterface(8)
    framed = Axi4sInterface(8)
    appout = Axi4sInterface(8)
    buffered = Axi4sInterface(8)
    totx = Axi4sInterface(8)
    o = Axi4sInterface(8)

    rs232tx_input_inst = rs232tx(reset, clk, i, ser_in, baudDiv)
    rs232rx_input_inst = rs232rx(reset, clk, toskid, ser_in, baudDiv)
    skidbuffer_inst = axi4s_skidbuf(reset, clk, toskid, todeesc)
    deescaper_inst = axi4s_last_deescaper(reset, clk, todeesc, framed, frameError, 0xc0, 0x03)
    app_inst = application_test_str(reset, clk, framed, appout, mdio_in, mdio_out, mdio_tristate, mdio_clk)
    fifo_inst = axi4s_fifo(reset, clk, appout, buffered, 1024)
    escaper_inst = axi4s_last_escaper(reset, clk, buffered, totx, 0xc0, 0x03)
    rs232tx_output_inst = rs232tx(reset, clk, totx, ser_out, baudDiv)
    rs232rx_output_inst = rs232rx(reset, clk, o, ser_out, baudDiv)


    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(100000):
            yield clk.posedge
        raise StopSimulation("Simulation did not end successfully")

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
        i.ready.next = 1
        #raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data_in, test_last_in, test_delay_in);


    return clkgen, monitor, gen_reset,rs232tx_input_inst, rs232rx_input_inst, skidbuffer_inst, deescaper_inst, app_inst, fifo_inst, escaper_inst, rs232tx_output_inst, rs232rx_output_inst, write, read

tb = simulation_serial_and_escaping();
tb.config_sim(trace=True)
tb.run_sim();
