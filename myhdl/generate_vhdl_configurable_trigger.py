from myhdl import *


from component_configurable_trigger import configurable_trigger

def convert_configurable_trigger(hdl):
    reset = ResetSignal(0, active=1, isasync=True)
    clk = Signal(False)
    dataIn = Signal(intbv(0)[4:])
    referenceWord = Signal(intbv(0)[4:])
    care = Signal(intbv(0)[4:])
    trigged = Signal(False)
    
    configurable_trigger_inst = configurable_trigger(reset, clk, dataIn, referenceWord, care, trigged)
    configurable_trigger_inst.convert(hdl=hdl);


convert_configurable_trigger(hdl='VHDL')
