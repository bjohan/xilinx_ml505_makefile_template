from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_ethernet_fcs_generator import axi4s_ethernet_fcs_generator
from component_axi4s_ethernet_valid_framer import axi4s_ethernet_valid_framer
from component_axi4s_packet_fifo import axi4s_packet_fifo
import struct

test_data =     []
read_data =     []
read_last =     []
read_delay =    []

test_valid=     []


def load_binary_ethernet_file(fn):
    test_data = [1]
    read_data = [1]
    read_last = [1]
    read_delay = [1]

    test_valid= [1]
    tbdat = open(fn, 'rb')
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
    return test_data[1:], read_data[1:], read_last[1:], read_delay[1:], test_valid[1:]



for i in range(1):
    td, rd, l, d, v = load_binary_ethernet_file("tbdata/arp_request.bin")
    for j in range(4): #Blank out valid bit for checksum 
        v[61+j]=0
    test_data+=td
    read_data+=rd
    read_last+=l
    read_delay+=d
    test_valid+=v

@block
def test_axi4s_ethernet_fcs_generator():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    framed = Axi4sInterface(8);
    checked = Axi4sInterface(8);
 
    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)

    fcs = Signal(modbv(0)[32:])

    axi4s_ethernet_valid_framer_inst = axi4s_ethernet_valid_framer(reset, clk, rxdata, rx_dv, framed)
    axi4s_ethernet_fcs_generator_inst = axi4s_ethernet_fcs_generator(reset, clk,framed, checked, fcs)
    
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
    def read():
        yield reset.negedge
        checked.ready.next = 1
        while True:
            if checked.last and fcs == 0xEA3484AB:
                raise StopSimulation("Correct checksum calculated")
            yield clk.posedge


    @instance
    def write():
        yield reset.negedge
        for d, v in zip(test_data, test_valid):
            rx_dv.next = v
            rxdata.next = d
            yield clk.posedge
            


    return clkgen, gen_reset, monitor, axi4s_ethernet_valid_framer_inst, axi4s_ethernet_fcs_generator_inst, write, read



tb = test_axi4s_ethernet_fcs_generator();
tb.config_sim(trace=True)
tb.run_sim();
