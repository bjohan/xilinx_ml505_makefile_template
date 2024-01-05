from myhdl import *


from component_configurable_trigger import configurable_trigger

def convert_configurable_trigger(hdl):
    
    dataIn = Signal(intbv(0)[4:])
    andMask = Signal(intbv(0)[4:])
    orMask = Signal(intbv(0)[4:])
    trigAnd = Signal(False);
    trigOr = Signal(False);
    
    configurable_trigger_inst = configurable_trigger(dataIn, andMask, orMask, trigAnd, trigOr)
    configurable_trigger_inst.convert(hdl=hdl);


convert_configurable_trigger(hdl='VHDL')
