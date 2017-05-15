import time

class bus:
    components = []
    address = 0
    mode = 0
    data = 00

    def __init__(self):
        return

    def register(self, component):
        self.components.append(component)
        return

    def clock(self):
        #print("CLOCK")
        #time.sleep(0.1)
        if self.components:
            for i in self.components:
                if i.clock:
                    i.clock()
        return

    def event(self):
        if self.components:
            for i in self.components:
                if i.event:
                    if (i.event()):
                        break
        self.mode = 0
        return

    def readInMemory(self, address):
        self.mode = 1
        self.address = address
        self.data = 0
        self.event()
        return self.data

    def writeInMemory(self, address, data):
        self.mode = 2
        self.address = address
        self.data = data
        self.event()
        return
