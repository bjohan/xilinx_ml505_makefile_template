from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_ethernet_frame_check import axi4s_ethernet_frame_check
from component_axi4s_ethernet_valid_framer import axi4s_ethernet_valid_framer
import struct

test_data =     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3, 0xaa, 0xbb, 0xcc]
read_data =     [0xA0,       0xA2, 0xA3, 0xB0,             0xB3, 0xC0, 0xC1, 0xC2]
read_last =     [1,          0,    0,    1,                0,    0,    0,    1  ]
read_delay =    [0,          0,    0,    0,                0,    0,    0,    0  ]

test_valid=     [1,    0,    1,    1,    1,    0,    0,    1,    1,    1,    1,    0,    0,    0,    0]

tbdat = open("tbdata/arp_request.bin", 'rb')
dat = tbdat.read()
for i in range(len(dat)>>1):
    a = struct.unpack("H", dat[i*2:i*2+2])[0]
    valid = (a & 0x80) >> 7
    data = a >> 8
    test_data.append(data)
    if valid:
        read_data.append(data)
    read_delay.append(0)
    if test_valid[-1] == 1 and valid == 0:
        read_last[-1]=1
    read_last.append(0)
    test_valid.append(valid)


@block
def test_axi4s_ethernet_frame_check():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    framed = Axi4sInterface(8);
    checked = Axi4sInterface(8);
 
    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)

    frame_valid = Signal(False)

    axi4s_ethernet_valid_framer_inst = axi4s_ethernet_valid_framer(reset, clk, rxdata, rx_dv, framed)
    axi4s_ethernet_frame_check_inst = axi4s_ethernet_frame_check(reset, clk,framed, checked, frame_valid)
    
    

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
        checked.ready.next = 1
        #yield tbReceiveSequence(clk, o, read_data, read_last, read_delay);
        #raise StopSimulation("Simulation ended successfully")


    @instance
    def write():
        yield reset.negedge
        for d, v in zip(test_data, test_valid):
            rx_dv.next = v
            rxdata.next = d
            yield clk.posedge
            


    return clkgen, gen_reset, monitor, axi4s_ethernet_frame_check_inst, axi4s_ethernet_valid_framer_inst, write, read



tb = test_axi4s_ethernet_frame_check();
tb.config_sim(trace=True)
tb.run_sim();
