from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_function_debug_core import function_debug_core
#                   ident        set and trig mask                              set or trig mask                               arm
test_data_in =     [0xFFFFFFFF,  0x01, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00,      0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,      0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
test_last_in =     [1,           0,    0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    0,    1,         0,    0,    0,    0,    0,    0,    0,    1,]
test_delay_in =    [0,           0,    1,    1,    0,    0,    3,    0,         0,    1,    1,    0,    0,    3,    0,         0,    0,    0,    0,    0,    0,    0,    0]


@block
def test_function_debug_core():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    i = Axi4sInterface(32); 
    o = Axi4sInterface(32);

    debugData = Signal(modbv()[123:])
    print("debugdata", len(debugData)) 
    function_debug_core_inst = function_debug_core(reset, clk, i, o, debugData, 16)

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
        quit(0)
        #quit(-1)

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge
        while True:
            debugData.next = debugData + 1
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


    return clkgen, gen_reset, monitor, function_debug_core_inst, write, read



tb = test_function_debug_core();
tb.config_sim(trace=True)
tb.run_sim();
