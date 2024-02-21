from myhdl import *
from component_axi4s_address_switch import axi4s_address_switch
from component_axi4s_address_merge import axi4s_address_merge
from component_axi4s_address_branch import axi4s_address_branch
from component_function_debug_core import function_debug_core
from component_function_mdio_interface import function_mdio_interface
from interface_axi4s import Axi4sInterface



@block
def application_test_str(reset, clk, i, o, mdio_in, mdio_out_o, mdio_tristate_o, mdio_clk_o):
    mdio_out_r = Signal(False)
    mdio_tristate_r = Signal(False)
    mdio_clk_r = Signal(False)
    mdio_out = Signal(True)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)
    funcaddr= 0x01
    funcaddr2= 0x03
    funcaddr3= 0x05
    debug0 = Signal(modbv(0)[73:0])
    debug1 = Signal(modbv(0)[4:]) 

    i_debug0 = Axi4sInterface(8); 
    o_debug0 = Axi4sInterface(8);

    i_debug0_to_debug1 = Axi4sInterface(8); 
    o_debug0_to_debug1 = Axi4sInterface(8);

    i_debug1 = Axi4sInterface(8); 
    o_debug1 = Axi4sInterface(8);

    i_debug1_to_mdio0 = Axi4sInterface(8); 
    o_debug1_to_mdio0 = Axi4sInterface(8);

    i_mdio0 = Axi4sInterface(8); 
    o_mdio0 = Axi4sInterface(8);
    
    through = Axi4sInterface(8);
 
    axi4s_address_branch_inst = axi4s_address_branch(reset, clk, i, o, i_debug0, o_debug0, funcaddr, i_debug0_to_debug1, o_debug0_to_debug1)
    debug_core_inst0 = function_debug_core(reset, clk, i_debug0, o_debug0, debug0, 1024)
    
    axi4s_address_branch_inst2 = axi4s_address_branch(reset, clk, o_debug0_to_debug1, i_debug0_to_debug1, i_debug1, o_debug1, funcaddr2, i_debug1_to_mdio0, o_debug1_to_mdio0)
    debug_core_inst1 = function_debug_core(reset, clk, i_debug1, o_debug1, debug1, 512*8)

    axi4s_address_branch_inst3 = axi4s_address_branch(reset, clk, o_debug1_to_mdio0, i_debug1_to_mdio0, i_mdio0, o_mdio0, funcaddr3, through, through)
    mdio_interface_inst0 = function_mdio_interface(reset, clk, i_mdio0, o_mdio0, mdio_in, mdio_out, mdio_tristate, mdio_clk)

    @always_comb
    def comb():
        debug1.next = concat(mdio_clk_r, mdio_tristate_r, mdio_out_r, mdio_in)#Signal(modbv(-1)[13:0])
        mdio_out_o.next = mdio_out_r
        mdio_tristate_o.next = mdio_tristate_r
        mdio_clk_o.next = mdio_clk_r

    @always_seq(clk.posedge, reset=reset)
    def logic():
        mdio_out_r.next = mdio_out
        mdio_tristate_r.next = mdio_tristate
        mdio_clk_r.next = mdio_clk
        debug0.next=debug0+1
        #debug1.next=debug1+1

    return axi4s_address_branch_inst, debug_core_inst0, axi4s_address_branch_inst2, debug_core_inst1, axi4s_address_branch_inst3, mdio_interface_inst0, logic, comb
