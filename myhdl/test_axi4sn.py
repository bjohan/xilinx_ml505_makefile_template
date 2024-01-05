from myhdl import *


from component_axi4sn import axi4sn
@block
def test_axi4sn():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[32:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)
    
    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(False)
    tLastOut = Signal(False)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    axi4sn_inst = axi4sn(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tDataOut, tValidOut, tReadyIn, tLastOut, 4)


    @instance
    def read():
        print("Read process started")
        for i in range(3):
            yield clk.negedge
        for i in range(10):
            if not tValidOut:
                print("Waiting for tvalidout")
                yield tValidOut.posedge
                print("Got tvalidout")
            yield clk.negedge
            tReadyIn.next = 1
            yield clk.negedge
            tReadyIn.next = 0
            yield clk.negedge
            tReadyIn.next = 1
            yield clk.negedge
            yield tValidOut.negedge
            print("Waiting for tvalidout")
            yield tValidOut.posedge
            print("Got tvalidout");
            yield tValidOut.negedge
            yield clk.negedge
            tReadyIn.next = 0;

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = 0
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.negedge
        print("Starting to transmit")
        for b in [0xA3A2A1A0, 0xB3B2B1B0, 0xC3C2C1C0, 0xD3D2D1D0, 0xE3D2D1E0, 0xF3F2F1F0]:
            print("Transmitting ", b)
            tDataIn.next = b
            if b in [0xB3B2B1B0, 0xE3D2D1E0]:
                tLastIn.next = 1
            else:
                tLastIn.next = 0

            tValidIn.next = 1
            yield clk.negedge
            print("Waiting for ready")
            for i in range(100):
                if tReadyOut:
                    break
                yield clk.negedge
           
            else:
                raise StopSimulation("tReadyOut not set")    
            yield clk.negedge
            tValidIn.next = 0
        print("extra clocks")
        for i in range(3):
            yield clk.negedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, axi4sn_inst, write, read

tb = test_axi4sn();
tb.config_sim(trace=True)
tb.run_sim();
