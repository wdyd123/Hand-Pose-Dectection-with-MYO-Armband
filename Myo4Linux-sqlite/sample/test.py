import serial
import time
from packet import Packet
from utilities import *

Packet = pack('BH', 0x00, 0x17)
print(Packet)