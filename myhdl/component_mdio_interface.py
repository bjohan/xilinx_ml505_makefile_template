from myhdl import *

@block
def mdio_interface(reset, clk, i, o, t, mdc, rw, phyAddr, regAddr, dataWrite, dataOut, start, busy, baudDivHalf=5):
    baudTick = Signal(False)
    baudCnt = Signal(intbv(min=0, max=2**24))
    currentBit = Signal(intbv(0, min=0, max=33));
    completeWord = Signal(intbv(0)[33:])
    read = Signal(False)
    mdcs = Signal(False)
    dataOuts = Signal(modbv(0)[len(dataOut):])

    @always_comb
    def out_reg():
        dataOut.next = dataOuts

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if not reset:
            if currentBit > 0:
                baudTick.next = False
                baudCnt.next = baudCnt +1;
                if baudCnt == baudDivHalf:
                    baudCnt.next = 0
                    if mdcs:
                        mdcs.next = False
                        mdc.next = False
                        baudTick.next = True
                    else:
                        mdcs.next = True
                        mdc.next = True

            if currentBit == 0:
                busy.next = False
                #setup gransfer
                read.next = rw
                completeWord.next[2:0] = 0b10 #start seq
                if rw: #read
                    completeWord.next[4:2] = 0b10 #read opcode
                else:
                    completeWord.next[4:2] = 0b01 #write opcode
                completeWord.next[9:4] = phyAddr
                completeWord.next[14:9] = regAddr
                completeWord.next[16:14] = 0b10
                completeWord.next[33:16] = dataWrite
                o.next = 0 #start bit
                t.next  = 0
                if start:
                    busy.next = True
                    currentBit.next = 1
            elif currentBit > 0 and currentBit < 14 and baudTick:
                #transmit start, opcode and addresses
                o.next = completeWord[currentBit]
                currentBit.next = currentBit + 1
                if currentBit == 13 and read:
                    o.next = 0
            elif currentBit >= 14 and currentBit < 17 and baudTick and read:
                o.next = 0
                #if read, set tristate and skip leading zero
                t.next = 1
                currentBit.next = currentBit + 1
            elif currentBit >= 17 and currentBit < 33 and baudTick and read:
                #read response
                t.next = 1
                dataOuts.next = dataOuts << 1
                dataOuts.next[0] = i
                #completeWord.next[currentBit] = i
                if currentBit == 32:
                    currentBit.next = 0
                else:
                    currentBit.next = currentBit + 1
            elif currentBit >= 14 and currentBit < 33 and baudTick and not read:
                t.next = 0
                #write TA and register data
                o.next = completeWord[currentBit]
                if currentBit==32:
                    currentBit.next = 0
                else:
                    currentBit.next = currentBit + 1

    return logic, out_reg
