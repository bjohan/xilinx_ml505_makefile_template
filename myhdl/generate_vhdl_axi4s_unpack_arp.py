from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_unpack_arp import axi4s_unpack_arp

def convert_axi4s_unpack_arp(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)

    ethernetPayload = Axi4sInterface(8);
    arpPayload = Axi4sInterface(8);


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

    axi4s_unpack_arp_inst = axi4s_unpack_arp(reset, clk, ethernetPayload, arpPayload, hardware_type, protocol_type, hardware_size, protocol_size, opcode, 
                                                                            sender_mac, sender_ip, target_mac, target_ip, arpHeaderValid, arpHeaderReady)

    axi4s_unpack_arp_inst.convert(hdl=hdl);


convert_axi4s_unpack_arp(hdl='VHDL')
