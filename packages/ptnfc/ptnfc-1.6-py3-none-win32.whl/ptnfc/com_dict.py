from serial.tools.list_ports_windows import *


class ComAddressDict(dict):

    def __init__(self):
        plist = list(comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")
        else:
            for p in plist:
                if p.location:
                    self[p.location] = p.name
