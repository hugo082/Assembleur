import sys
import os
import Queue
from threading import Thread
from bus import bus

class io:
    SCR_WIDTH = 80
    SCR_HEIGHT = 25
    SCR_MEM_MIN = 16892
    SCR_MEM_MAX = SCR_MEM_MIN + SCR_WIDTH * SCR_HEIGHT

    IN_MEM_MIN = 16636
    IN_MEM_MAX = 16891
    IN_MEM_LEN = IN_MEM_MAX - IN_MEM_MIN

    pixel = 0

    inputQueue = Queue.Queue(IN_MEM_LEN)

    def __init__(self, bus):
        self.thr = Thread(target=self.listenKeyboard)
        self.keyboardListening = False
        self.bus = bus
        bus.register(self)
        self.clear()
        return

    def addressToPosition(self, address):
        """
        Convert ram address memory to (x, y) position
        """
        y = 0
        address -= self.SCR_MEM_MIN - 1
        while address > self.SCR_WIDTH:
            y += 1
            address -= self.SCR_WIDTH
        return (address, y + 1)

    def event(self):
        if self.bus:
            ad = self.bus.address
            if (self.bus.mode == 2 and ad >= self.SCR_MEM_MIN and ad <= self.SCR_MEM_MAX):
                (x, y) = self.addressToPosition(ad)
                self.updatePixelWithBusData(x, y)
                self.flushScreen()
            if (self.bus.mode == 1 and ad >= self.IN_MEM_MIN and ad <= self.IN_MEM_MAX):
                self.bus.data = self.readInput(ad)
                return True
        return False

    def clock(self): # TODO
        #print('Clock on I/O')
        return

    def getPixelInMemory(self, x, y):
        """
        Get pixel at position (x,y) with ram memory
        """
        ad = self.SCR_MEM_MIN + (y * self.SCR_WIDTH) + x
        self.pixel = self.bus.readInMemory(ad)
        return

    def resetCursorPosition(self):
        """
        Reset position of current cursor
        """
        y = self.SCR_HEIGHT + 2
        sys.stdout.write("\033[%d;%dH" % (y, 0))
        return

    def updatePixelWithBusData(self, x, y):
        """
        Update pixel at position with bus data
        """
        u = unichr(self.bus.data) # int to ASCII
        u.encode('utf-8')
        #print(str(x) + " - " + str(y) + " : " + str(u))
        sys.stdout.write("\033[%d;%dH%s" % (y, x, u))
        return

    def updatePixel(self, x, y):
        """
        Update pixel at position with ram memory
        """
        self.getPixelInMemory(x, y)
        self.updatePixelWithBusData(x, y)
        return

    def updateFullScreen(self):
        """
        Update all pixel of the screen with ram memory
        """
        for x in range(self.SCR_WIDTH):
            for y in range(self.SCR_HEIGHT):
                updatePixel(x, y)
        self.flushScreen()
        return

    def clear(self):
        """
        Clear screen
        """
        os.system('clear')
        return

    def flushScreen(self):
        """
        Update screen with last write
        """
        self.resetCursorPosition()
        sys.stdout.flush()
        return

    cInputIndex = IN_MEM_MIN

    def keypressEvent(self, key):
        """
        On keypres event
        """
        if (not self.inputQueue.full()):
            self.inputQueue.put(key)

    def readInput(self, index):
        if (self.inputQueue.empty()):
            return 0
        inputIndx = self.IN_MEM_MAX - index
        key = self.inputQueue.get(inputIndx)
        return key

    def debugInputMemory(self): # For developpement
        res = ""
        while not self.inputQueue.empty():
            res += chr(self.readInput(self.IN_MEM_MIN))
        print(res)

    def pushWordInMemory(self, word): # For developpement
        for c in word:
            self.keypressEvent(ord(c))

    def listenKeyboard(self):
        """
        Listening keyboard sync
        """
        getch = _Getch()
        while self.keyboardListening:
            ch = getch()
            if not ch or ch == chr(4):
                break
            self.keypressEvent(ord(ch))

    def startKeyboardListening(self):
        """
        Start listening keyboard async
        """
        self.keyboardListening = True
        self.thr.start()

    def stopKeyboardListening(self):
        """
        Stop listening keyboard async
        """
        self.keyboardListening = False
        print("Press any key to quit")

class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
