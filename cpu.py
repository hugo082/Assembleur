from bus import bus
from alu import alu

import time

class cpu:
    FINISH = -1
    ER_FINISH_OP = -2
    ER_EMPTY_REGISTER = -3

    HEAP_MEM_MIN = 65525

    bus
    alu
    heapIdx = HEAP_MEM_MIN
    finish_code = 0
    pc = 0
    op = 0x0000
    register = 0x0000
    value = 0x0000

    registers = {
    0x13 : 0b0000 # 0.Zero 1.Signed 2.Overflow 3.Parity 4.Condition
    }

    def getSRegisterByIndex(self, index):
        """
        Get flag at index
        """
        return(self.registers[0x13] >> index)% 2

    def setSRegisterByIndex(self, index, value):
        """
        Set flag at index
        """
        if (self.getSRegisterByIndex(index) != value):
            if (index != 0):
                self.registers[0x13] += (2 * value - 1) * pow(2,index)
            else:
                self.registers[0x13] += (2 * value - 1)

    def loadInMemoryWithFile(self, filename = 'bin'):
        """
        Load binary file in memory for execution
        """
        file = open(filename, 'r')
        chaineBin = file.read()
        file.close()
        size = len(chaineBin)/32
        for i in range(size):
            self.bus.writeInMemory(i, int(chaineBin[i * 32:(i + 1) * 32], 2))
        return

    def setSRegisterCondition(self, value):
        """
        Compute condition flag
        """
        self.registers[0x13] = 0b0000
        self.setSRegisterByIndex(4, value)

    def setArithmetic(self):
        """
        Compute flags
        """
        buf = self.getRegisterWithIndex(self.register)
        self.registers[0x13] = 0b0000
        if (buf == 0):
            self.setSRegisterByIndex(0, 1)
        elif (buf < 0):
            self.setSRegisterByIndex(1, 1)
        if (buf > 0xFFFF):
            self.setSRegisterByIndex(2, 1)
        self.setSREgisterParity(buf)

    def setSREgisterParity(self, v):
        """
        Compute parity flag
        """
        v ^= v >> 1
        v ^= v >> 2
        v = (v & 0x11111111) * 0x11111111
        self.setSRegisterByIndex(3, ((v >> 28) & 1) != 1)

    def iSet(self):
        #print("SET " + str(self.value) + " in " + str(self.register))
        self.registers[self.register] = self.value
        return
    def iMove(self):
        #print("MV " + str(self.value) + " to register " + str(self.register))
        self.registers[self.register] = self.value
        return
    def iLoad(self):
        #print("LOAD(LD) at " + str(self.value) + " in " + str(self.register))
        self.registers[self.register] = self.bus.readInMemory(self.value)
        return
    def iSave(self):
        #print("SAVE(ST) " + str(self.getRegisterWithIndex(self.register)) + " in " + str(self.value))
        self.bus.writeInMemory(self.value, self.getRegisterWithIndex(self.register))
        return
    def iJmp(self):
        #print("Branchement(JMP) " + str(self.value) + " - " + str(self.register))
        if (self.register != 0):
            self.pushAddressOnHeap(self.pc)
        self.pc = self.value
        return
    def iJmz(self):
        #print("Branchement(JMZ) " + str(self.register) + "si Zflag a 1")
        if (self.getSRegisterByIndex(0)):
            self.pc = self.value
        return
    def iJmo(self):
        #print("Branchement(JMO) " + str(self.register) + "si Oflag a 1")
        if (self.getSRegisterByIndex(2)):
            self.pc = self.value
        return
    def iJmc(self):
        #print("Branchement(JMC) " + str(self.value) + " if " + str(self.getSRegisterByIndex(4)))
        if (self.getSRegisterByIndex(4)):
            self.pc = self.value
        return
    def iOr(self):
        #print(hex(self.register) + " OR(OR) " + hex(self.value) + " in " + str(self.register))
        self.registers[self.register] |= self.value
        self.setArithmetic()
        return
    def iAnd(self):
        #print(hex(self.register) + " AND(AND) " + hex(self.value) + " in " + str(self.register))
        self.registers[self.register] &= self.value
        self.setArithmetic()
        return
    def iXor(self):
        #print(hex(self.register) + " XOR(XOR) " + hex(self.value) + " in " + str(self.register))
        self.registers[self.register] ^= self.value
        self.setArithmetic()
        return
    def iNot(self):
        #print(hex(self.register) + " NOT(NOT) " + hex(self.value) + " in " + str(self.register))
        self.registers[self.register] = ~self.getRegisterWithIndex(self.register)
        self.setArithmetic()
        return
    def iAdd(self):
        #print("ADD " + str(self.value) + " IN " + hex(self.register))
        self.registers[self.register] += self.value
        self.setArithmetic()
        return
    def iSub(self):
        self.registers[self.register] -= self.value
        self.setArithmetic()
        return
    def iMul(self):
        #print(hex(self.register) + " - " + str(self.registers[self.register]) + " Multi(MUL) " + str(self.value))
        self.registers[self.register] *= self.value
        self.setArithmetic()
        return
    def iDiv(self):
        self.registers[self.register] /= self.value
        self.setArithmetic()
        return
    def iLt(self):
        #print(hex(self.register) + " - " + str(self.registers[self.register]) + " LessThan(LT) " + str(self.value) + " in S")
        self.setSRegisterCondition(self.registers[self.register] < self.value)
        return
    def iGt(self):
        #print(hex(self.register) + " GreaterThan(GT) " + hex(self.value) + " in S")
        self.setSRegisterCondition(self.registers[self.register] > self.value)
        return
    def iLe(self):
        #print(str(self.registers[self.register]) + " LessThanOrEqual(LE) " + str(self.registers[self.value]) + " in " + str(self.registers[self.register] <= self.registers[self.value]))
        self.setSRegisterCondition(self.registers[self.register] <= self.value)
        return
    def iGe(self):
        #print(hex(self.register) + " GreaterThanOrEqual(GE) " + hex(self.value) + " in S")
        self.setSRegisterCondition(self.registers[self.register] >= self.value)
        return
    def iEq(self):
        if self.value == 71:
            print(hex(self.register) + " - " + str(self.registers[self.register]) + " Equal(EQ) " + str(self.value) + " in S")
        self.setSRegisterCondition(self.registers[self.register] == self.value)
        return
    def iEz(self):
        #print(str(self.registers[self.register]) + "(" + hex(self.register) + ") EqualZero(EZ) in S")
        self.setSRegisterCondition(self.registers[self.register] == 0)
        return
    def iNz(self):
        #print(hex(self.register) + " DifferentZero(NZ) in S")
        self.setSRegisterCondition(self.registers[self.register]!= 0)
        return
    def iNop(self):
        #print("Nothing(NOP)")
        return
    def iHlt(self):
        #print("Finish : " + str(self.pc))
        self.finish_code = self.FINISH
        return
    def iHft(self): # TODO
        #print("QuitFunction(HFT)")
        self.pc = self.popAddressOnHeap()
        return

    def pushAddressOnHeap(self, value):
        self.heapIdx += 1
        self.bus.writeInMemory(self.heapIdx, value)
        return
    def popAddressOnHeap(self):
        v = self.bus.readInMemory(self.heapIdx)
        self.heapIdx -= 1
        return v

    instructions = {
    0x00 : iNop, # NOP
    0x01 : iJmp, # JMP
    0x02 : iJmz, # JMZ
    0x03 : iJmo, # JMO
    0x04 : iJmc, # JMC
    0x05 : iSet, # SET
    0x06 : iLoad, # LD
    0x07 : iSave, # ST
    0x08 : iMove, # MV
    0x09 : iAdd,
    0x0A : iSub,
    0x0B : iMul,
    0x0C : iDiv,
    0x0D : iOr,
    0x0E : iAnd,
    0x0F : iXor,
    0x10 : iNot,
    0x11 : iHlt, # HLT
    0x12 : iHft, # Quit function
    0x13 : iLt,
    0x14 : iGt,
    0x15 : iLe,
    0x16 : iGe,
    0x17 : iEq,
    0x18 : iEz,
    0x19 : iNz
    }

    def __init__(self, bus):
        self.bus = bus
        self.bus.register(self)
        self.alu = alu(self.registers)
        return

    def register(self, component): # TODO
        return

    def event(self): # TODO
        return

    def run(self):
        """
        Run execution
        """
        while (self.finish_code == 0):
            self.bus.clock()
            #time.sleep(1)
        if (self.finish_code != self.FINISH):
            print("Exit With EROR. Code : " + str(self.finish_code) + " at : " + str(self.pc))
        else:
            print("Exit. (SUCCESS)")
        return

    def clock(self):
        """
        Execute an instrcution
        """
        self.fetch()
        #print(str(self.pc) + " : " + str(self.op) + " - " + str(self.register) + " - " + str(self.value))
        if (self.op):
            self.instructions[self.op](self)
        return

    def fetch(self):
        """
        Load and decode binary instrcution
        """
        #print("PC :" + str(self.pc))
        self.bus.address = self.pc
        self.bus.mode = 1
        self.bus.event()
        code = self.bus.data
        if (code == 0):
            self.finish_code = self.ER_FINISH_OP
            return
        self.op = code >> 24
        self.register = (code & 0x00FF0000) >> 16
        self.value = code & 0x0000FFFF
        self.pc = self.pc + 1
        self.computeValue()
        return

    def computeValue(self):
        """
        Compute value : is register or value/address
        """
        if (self.op < 128):
            self.value = self.getRegisterWithIndex(self.value)
            if (self.finish_code != 0):
                print("ERROR : " + str(self.op) + " - " + str(self.pc))
        else:
            self.op -= 128
        return

    def getRegisterWithIndex(self, index):
        """
        Return value in a register.
        Stop program if register is empty.
        """
        if (index == 0x00): # null value
            return 0
        if (index == 0x18): # current heap address
            return self.bus.readInMemory(self.heapIdx)
        if (index == 0x19): # current PC
            return self.pc
        if index in self.registers:
            return self.registers[index]
        print("Impossible to read register : " + str(index))
        self.finish_code = self.ER_EMPTY_REGISTER
        return 0

    def debufFlags(self):
        print("F(CPOSZ): " + bin(self.registers[0x13])[2:].zfill(5))
        return

    def debufRegisters(self):
        res = "{\n"
        for reg in self.registers:
            res += "  "
            if (reg == 0x13):
                res += "F(CPOSZ) : " + bin(self.registers[0x13])[2:].zfill(5)
            else:
                res += str(reg) + " : " + str(self.registers[reg])
            res += "\n"
        print(res + "}")
        return
