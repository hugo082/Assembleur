from bus import bus

class ram:
    bus = 0
    memory = [0] * 65535

    def __init__(self, bus):
        self.bus = bus
        bus.register(self)
        return

    def event(self):
        if self.bus:
            if self.bus.mode == 1:
                self.read()
            elif self.bus.mode == 2:
                self.write()
        return

    def read(self):
        #print("Read at : " + str(self.bus.address) + " - " + str(self.memory[self.bus.address]))
        self.bus.data = self.memory[self.bus.address]
        return

    def write(self):
        #print("Write at : " + str(self.bus.address) + " - " + str(self.bus.data))
        self.memory[self.bus.address] = self.bus.data
        return

    def clock(self): # TODO
        #print('Clock on RAM')
        return

    def debugMemory(self):
        res = "{\n"
        for index, value in enumerate(self.memory):
            if value != 0:
                res += "  " + str(index) + " : " + str(value) + "\n"
        res += "}"
        print(res)
