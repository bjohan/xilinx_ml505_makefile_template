import time
import functions.functions
import struct
import threading
import queue

class DeEscaper:
    def __init__(self, esc, end):
        self.esc = esc;
        self.end = end;
        self.data = []
        
    def addData(self, d):
        self.data+=d

    def getFrame(self):
        escaped = False
        nextIsLast = False
        payload = []
        consumed = 0
        for d in self.data:
            consumed+=1
            if escaped:
                if d == self.esc:
                    payload.append(d)
                    if nextIsLast:
                        self.data = self.data[consumed:]
                        return bytes(payload)
                elif d == self.end:
                    nextIsLast = True
                else:
                    raise ValueError("Corrpupt stream, only escape and end shall be escaped")
                escaped = False
            elif d == self.esc:
                escaped=True
            else:
                escaped=False
                payload.append(d)
                if nextIsLast:
                    self.data = self.data[consumed:]
                    return bytes(payload)
        return None

class Escaper:
    def __init__(self, esc, end):
        self.esc = esc
        self.end = end

    def escaped(self, data):
        if data == self.esc:
            return [self.esc, data]
        return [data]

    def generateEscapedrame(self, data):
        output = []
        for d in data[0:-1]:
            output+= self.escaped(d)
        output+=[self.esc, self.end]
        output+=self.escaped(data[-1])
        return bytes(output)

class DebugCore:
    def __init__(self):
        pass
    
    def setup(self, frame):
        pass

class FrameReaderThread(threading.Thread):
    def __init__(self, reader, deescaper, frameMapper, start = True):
        super().__init__()
        self.reader = reader;
        self.frameMapper = frameMapper
        self.stopEvent = threading.Event()
        self.deescaper = deescaper
        if start:
            self.start()
    
    def run(self):
        while True:
            if self.stopEvent.is_set():
                break
            try:
                d = self.reader.read(1)
                if len(d):
                    #print("Got", d)
                    self.deescaper.addData(d)
                    frame = self.deescaper.getFrame()
                    if frame is not None:
                        #print("Got", frame)
                        self.frameMapper.processFrame(frame)
            except TimeoutError:
                pass

    def stop(self):
            self.stopEvent.set()

class FrameWriterThread(threading.Thread):
    def __init__(self, writer, escaper, start=True):
        super().__init__()
        self.writer = writer
        self.q = queue.Queue()
        self.stopEvent = threading.Event()
        self.escaper=escaper
        if start:
            self.start()

    def writeFrame(self, frame):
        self.q.put(frame)

    def run(self):
        while True:
            if self.stopEvent.is_set():
                break
            try:
                frame = self.q.get(timeout=0.1)
                encoded = self.escaper.generateEscapedrame(frame)
                #print("Sending", encoded)
                self.writer.write(encoded)
            except queue.Empty:
                pass

    def stop(self):
        self.stopEvent.set()

class InitHelper:
    def __init__(self, writer):
        self.bc = 0xff
        self.frames = {}
        self.rxFrames = 0
        self.writer = writer
        self.t0=None
        
    def startInitSequence(self):
        self.t0 = time.time()
        self.writer.writeFrame([self.bc])

    def isComplete(self):
        """Check if exactly two of each frame has ben received"""
        complete=True;
        for frame in self.frames:
            if self.frames[frame] != 2:
                complete=False
        return complete

    def addInitFrame(self, frame):
        self.rxFrames+=1 

        if frame in self.frames:
            self.frames[frame]+=1
        else:
            self.frames[frame]=1

        if self.rxFrames == 2:
            self.writer.writeFrame([self.bc])

        if self.rxFrames >= 4:
            if self.isComplete():
                print("Got all initialization frames in", time.time()-self.t0)
                #print(self.frames)
                return True
        return False

class FrameBuffer:
    def __init__(self):
        self.q = queue.Queue()

    def processFrame(self, frame):
        self.q.put(frame)

    def getFrame(self, timeout=1):
        return self.q.get(timeout=timeout)
        

class MappingFrameBuffer:
    def __init__(self, writer):
        self.writer = writer
        self.init = InitHelper(writer)
        self.functionMap = {}
        self.bc = 0xff
        self.initDoneEvent = threading.Event()

    def waitInitComplete(self):
        self.initDoneEvent.wait()

    def startInitSequence(self):
        self.init.startInitSequence()

    def getAddressAndPayload(self, frame):
        addr = []
        nAddrBytes = 0
        for b in frame:
            if b==self.bc:
                break
            addr.append(b)
            nAddrBytes+=1
        payload = frame[nAddrBytes+1:]
        return bytes(addr), bytes(payload)

    def processFrame(self, frame):
        if len(self.functionMap) == 0:
            if self.init.addInitFrame(frame):
                self.buildFunctionMap(self.init.frames)
        else:
            address, payload = self.getAddressAndPayload(frame)
            self.functionMap[address].put(payload)

    def buildFunctionMap(self, frames):
        for frame in frames:
            addr, payload = self.getAddressAndPayload(frame)
            if len(addr) == 0:
                pass
            else:
                if addr not in self.functionMap:
                    self.functionMap[addr] = functions.functions.functionMap[int.from_bytes(payload)](addr, self.writer)
                else:
                    self.functionMap[addr].setup(payload)
        print("Init complete, functionmap:")
        print(self.functionMap)
        self.initDoneEvent.set()


class FunctionInterface:
    def __init__(self, reader, writer):
        """Function interface. reader object with read method to read from fpga. writer has write method to write"""
        self.fw = FrameWriterThread(writer, Escaper(0xc0, 0x03))
        self.frameMapper = MappingFrameBuffer(self.fw)
        self.fr = FrameReaderThread(reader, DeEscaper(0xc0, 0x03), self.frameMapper)
        self.frameMapper.startInitSequence()
        self.frameMapper.waitInitComplete()

    def stop(self):
        self.fw.stop()
        self.fr.stop()

