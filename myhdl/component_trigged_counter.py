from myhdl import *

@block
def trigged_counter(reset, clk, count, output, baudDiv=100):

    counter = Signal(modbv(0, min=0, max=255)[8:])
    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            if count:
                counter.next = counter + 1
            output.next = counter;    
        else:
            counter.next = 0


    return logic
