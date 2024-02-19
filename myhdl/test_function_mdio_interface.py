from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_function_mdio_interface import function_mdio_interface
#                   ident        send read reg 0   send write reg 0 to 0
test_data_in =     [0xFFFFFFFF,  1,                 0]
test_last_in =     [1,           1,                1]
test_delay_in =    [0,           0,                0]


@block
def test_function_mdio_interface():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    i = Axi4sInterface(32); 
    o = Axi4sInterface(32);

    mdio_in = Signal(True)
    mdio_out = Signal(False)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)

    function_mdio_interface_inst = function_mdio_interface(reset, clk, i, o, mdio_in, mdio_out, mdio_tristate, mdio_clk)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1


    @instance
    def monitor():
        for i in range(3000):
            yield clk.posedge
        print("Simulation did not end successfully")
        quit(0)
        #quit(-1)

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
        o.ready.next = 1
        #yield tbReceiveSequence(clk, o, test_data, test_last, test_delay_out);
        #raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        yield tbTransmitSequence(clk, i, test_data_in, test_last_in, test_delay_in);


    return clkgen, gen_reset, monitor, function_mdio_interface_inst, write, read



tb = test_function_mdio_interface();
tb.config_sim(trace=True)
tb.run_sim();
