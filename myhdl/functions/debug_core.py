import struct
from functions.function_ids import functionId
class DebugCore:
    def __init__(self, addr):
        self.addr = addr
        print("Created Debug Core with address:", self.addr)
    
    def setup(self, frame):
        (fid, self.width, self.depth)=struct.unpack("III", frame[0:12])
        if fid != functionId['debug_core']:
            raise ValueError("Invalid function id for debug core")
        print("Setup debugcore with bus width:", self.width, "fifo depth:", self.depth)
        

