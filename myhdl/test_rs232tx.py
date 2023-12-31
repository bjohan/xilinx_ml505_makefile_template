from myhdl import *


from component_rs232tx import rs232tx
@block
def test_rs232tx():

    clk = Signal(False)
    toTx = Signal(intbv(0xAA, min=0, max=256))
    txValid = Signal(False)
    txReady = Signal(False)
    txBusy = Signal(False)
    txd = Signal(False)
    #reset = ResetSignal(True)
    reset = ResetSignal(0, active=1, isasync=False)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    rs232tx_inst = rs232tx(reset, toTx, txValid, txReady, txBusy, txd, clk, 5)

    @instance
    def stimulus():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = False
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.negedge
        print("Starting to transmit")
        for b in [0xAA, 0x00, 0x01, 0x55, 0xFF, 0xF0, 0x0F]:
            print("wainting for txready")
            if not txReady:
                yield txReady.posedge
            print("Transmitting data")
            yield clk.negedge
            print("sending", b)
            toTx.next = b
            txValid.next = True
            print("Waiting for ack")
            yield txReady.negedge, delay(30)
            if txReady:
                raise StopSimulation("txValid did not deassert")
            yield clk.negedge
            print("Deasserting")
            txValid.next = False
        print("wainting for txready")
        if not txReady:
            yield txReady.posedge
        print("extra clocks")
        for i in range(3):
            yield clk.negedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return clkgen, rs232tx_inst, stimulus

tb = test_rs232tx();
tb.config_sim(trace=True)
tb.run_sim();
#traceSignals.name = "test_rs232tx"
#t = traceSignals(test_rs232tx)
#sim = Simulation(t)
#sim.run()
