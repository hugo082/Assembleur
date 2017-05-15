#import tkinter
import time

from bus import bus
from cpu import cpu
from ram import ram
from compiler import compiler
from io import io

compiler = compiler()
bus = bus()
cpu = cpu(bus)
ram = ram(bus)
io = io(bus)

def print_help():
    print("  Command :")
    print("    compile")
    print("    run")
    print("    keyboard")
    print("        Start / Stop l'ecoute du clavier")
    print("        (Pour stoppper l'ecoute du clavier, appuyer sur une touche apres l'avoir arrete.)")
    print("    input")
    print("        Simuler le clavier.")
    print("    debug")
    print("    help")
    print("    exit")

print("Enter 'help' for more informations.")
cmd = raw_input("-Cmd : ")
isCompile = False
while cmd != "exit":
    if (cmd == "compile"):
        filename = raw_input("  file name : ")
        isCompile = compiler.parseFile(filename)
    elif (cmd == "keyboard"):
        if (io.keyboardListening):
            io.stopKeyboardListening()
            print("  Stoped")
        else:
            io.startKeyboardListening()
            print("  Started")
    elif (cmd == "input"):
        words = raw_input("  text a ajouter dans la memoire : ")
        io.pushWordInMemory(words)
    elif (cmd == "run"):
        if (isCompile):
            if (not io.keyboardListening):
                cmd = raw_input("  Keyboard listening stopped. Start ? (Y)")
                if (cmd == "Y"):
                    io.startKeyboardListening()
                    print("  Started")
            io.clear()
            cpu.loadInMemoryWithFile()
            cpu.run()
            io.stopKeyboardListening()
        else:
            print("  You must compile a file before")
    elif (cmd == "help"):
        print_help()
    elif (cmd == "debug"):
        print("  Debug Flags :")
        cpu.debufFlags()
        print("  Debug Input Memory :")
        io.debugInputMemory()
        print("  Debug Registers :")
        cpu.debufRegisters()
        print("  Debug Memory :")
        ram.debugMemory()
    else:
        print("  Command not found")
    cmd = raw_input("-Cmd : ")
print("Quit.")
