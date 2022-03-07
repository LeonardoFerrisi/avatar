# Intented for usage with ubuntu

import os
import time
from subprocess import call
from sys import platform
from platform_nodes import WINDOWS_NODE, LINUX_NODE

# THIS IS THE LINUX version of RUN

# TODO: Add options menu to select boards to stream from, COM ports, serial ports if need be, etc...

class MASTER:
    def __init__(self):
        if platform == "linux" or platform == "linux2":
            # run linux
            linux = LINUX_NODE()

        elif platform == "win32":
            windows = WINDOWS_NODE()

        else:
            raise Exception("Only linux and windows are supported")


if __name__ == "__main__":
    m = MASTER()




