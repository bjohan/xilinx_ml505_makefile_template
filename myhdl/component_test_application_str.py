from myhdl import *
from component_axi4s_address_switch import axi4s_address_switch
from component_axi4s_address_merge import axi4s_address_merge
from component_axi4s_address_branch import axi4s_address_branch
from interface_axi4s import Axi4sInterface
from component_function_debug_core import function_debug_core



@block
def test_application_str(reset, clk, i, o):
    funcaddr= 0x01
    funcaddr2= 0x03
    debug = Signal(modbv(0)[73:0])
    debug2 = Signal(modbv(-1)[13:0])

    i_prev = Axi4sInterface(8); 
    o_prev = Axi4sInterface(8);
    i_func = Axi4sInterface(8); 
    o_func = Axi4sInterface(8);
    i_next = Axi4sInterface(8); 
    o_next = Axi4sInterface(8);
    through = Axi4sInterface(8);
    i_func2 = Axi4sInterface(8); 
    o_func2 = Axi4sInterface(8);
 
    axi4s_address_branch_inst = axi4s_address_branch(reset, clk, i, o, i_func, o_func, funcaddr, i_next, o_next)
    debug_core_inst = function_debug_core(reset, clk, i_func, o_func, debug, 1024)
    
    axi4s_address_branch_inst2 = axi4s_address_branch(reset, clk, o_next, i_next, i_func2, o_func2, funcaddr2, through, through)
    debug_core_inst2 = function_debug_core(reset, clk, i_func2, o_func2, debug2, 512)


    @always_seq(clk.posedge, reset=reset)
    def logic():
        debug.next=debug+1
        debug2.next=debug2+1

    return axi4s_address_branch_inst, debug_core_inst, axi4s_address_branch_inst2, debug_core_inst2, logic
