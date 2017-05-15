#import tkinter
import sys
import time

from bus import bus
from cpu import cpu
from ram import ram
from compiler import compiler
from io import io

compiler = compiler()
bus = bus()
cpu = cpu(bus)
io = io(bus)
ram = ram(bus)
#io.pushWordInMemory("B")
#io.pushWordInMemory("Bonjour Comment ca va ?")

if (not compiler.parseFile("instructions.txt", "bintest")):
    sys.exit(0)

cpu.loadInMemoryWithFile("bintest")

io.startKeyboardListening()
cpu.run()
io.stopKeyboardListening()
#
# print("  Debug Flags :")
# cpu.debufFlags()
# print("  Debug Registers :")
# cpu.debufRegisters()
# print("  Debug Input Memory :")
# io.debugInputMemory()
# print("  Debug Memory :")
# ram.debugMemory()
