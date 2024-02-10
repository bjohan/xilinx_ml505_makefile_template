from myhdl import *
from component_axi4s_address_switch import axi4s_address_switch
from component_axi4s_address_merge import axi4s_address_merge
from interface_axi4s import Axi4sInterface
from component_function_debug_core import function_debug_core

t_State = enum('S_POLL_THROUGH', 'S_POLL_MERGE', 'S_TRANSFER_THROUGH', 'S_TRANSFER_MERGE');
t_MuxState = enum('S_POLL', 'S_THROUGH', 'S_MERGE') 


@block
def test_application_str(reset, clk, i, o):
    through = Axi4sInterface(len(i.data))
    loopaddr= 0x01
    loopin = Axi4sInterface(len(i.data))
    loopout = Axi4sInterface(len(i.data))
    debug = Signal(modbv(0)[73:0])

    addr_switch_inst = axi4s_address_switch(reset, clk, i, loopin, loopaddr, through)
    debug_core_inst = function_debug_core(reset, clk, loopin, loopout, debug, 128)
    addr_merge_inst = axi4s_address_merge(reset, clk, through, loopout, loopaddr, o)
    
    return addr_switch_inst, debug_core_inst, addr_merge_inst
