from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_axi4s_receive_ethernet import axi4s_receive_ethernet
from component_axi4s_unpack_ethernet import axi4s_unpack_ethernet
from component_axi4s_unpack_arp import axi4s_unpack_arp
from component_axi4s_pack_arp import axi4s_pack_arp
import struct

test_data =     [0xA0, 0xA1, 0xA2, 0xA3, 0xB0, 0xB1, 0xB2, 0xB3, 0xC0, 0xC1, 0xC2, 0xC3, 0xaa, 0xbb, 0xcc]
read_data =     []
read_last =     []
read_delay =    []

test_valid=     [1,    0,    1,    1,    1,    0,    0,    1,    1,    1,    1,    0,    0,    0,    0]


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
    print("Length of test data", len(rd))
    test_data+=td
    read_data+=rd
    read_last+=l
    read_delay+=d
    test_valid+=v

@block
def test_axi4s_pack_arp():
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
   
    rxdata = Signal(intbv(0)[8:])
    rx_dv = Signal(False)

    valids = Axi4sInterface(8);
    ethernetPayload = Axi4sInterface(8);
    arpPayload = Axi4sInterface(8);
    arpGenerated= Axi4sInterface(8);


    #Ethernet frame signals
    sfd = Signal(modbv(0)[8:])
    dst = Signal(modbv(0)[48:])
    src = Signal(modbv(0)[48:])
    etherType = Signal(modbv(0)[16:])

    ethernetHeaderValid = Signal(True)
    ethernetHeaderReady = Signal(True)


    #ARP frame signals
    hardware_type = Signal(modbv(0)[16:])
    protocol_type = Signal(modbv(0)[16:])
    hardware_size = Signal(modbv(0)[8:])
    protocol_size = Signal(modbv(0)[8:])
    opcode = Signal(modbv(0)[16:])
    sender_mac = Signal(modbv(0)[48:])
    sender_ip = Signal(modbv(0)[32:])
    target_mac = Signal(modbv(0)[48:])
    target_ip = Signal(modbv(0)[32:])

    arpHeaderValid = Signal(True)
    arpHeaderReady = Signal(True)



    packetLength = Signal(intbv(0)[16:])
    axi4s_receive_ethernet_inst = axi4s_receive_ethernet(reset, clk, rxdata, rx_dv, valids, packetLength)
    axi4s_unpack_ethernet_inst = axi4s_unpack_ethernet(reset, clk, valids, ethernetPayload, sfd, dst, src, etherType, ethernetHeaderValid, ethernetHeaderReady)
    
    axi4s_unpack_arp_inst = axi4s_unpack_arp(reset, clk, ethernetPayload, arpPayload, hardware_type, protocol_type, hardware_size, protocol_size, opcode, 
                                                                            sender_mac, sender_ip, target_mac, target_ip, arpHeaderValid, arpHeaderReady)

    axi4s_pack_arp_inst = axi4s_pack_arp(reset, clk, arpGenerated, hardware_type, protocol_type, hardware_size, protocol_size, opcode,
                                                    sender_mac, sender_ip, target_mac, target_ip, arpHeaderValid, arpHeaderReady); 

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
        quit(-1*0)

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
        arpPayload.ready.next = 1
        arpGenerated.ready.next = 1
        #valids.ready.next = 1
        #print("done")
        #yield tbReceiveSequence(clk, valids, read_data, read_last, read_delay);
        #for i in range(10):
        #    yield clk.posedge
        #raise StopSimulation("Simulation ended successfully")

    @instance
    def write():
        yield reset.negedge
        for d, v in zip(test_data, test_valid):
            rx_dv.next = v
            rxdata.next = d
            yield clk.posedge

    return clkgen, gen_reset, monitor, axi4s_receive_ethernet_inst, axi4s_unpack_ethernet_inst, axi4s_unpack_arp_inst, axi4s_pack_arp_inst, write, read



tb = test_axi4s_pack_arp();
tb.config_sim(trace=True)
tb.run_sim();
