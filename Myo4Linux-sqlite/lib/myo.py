import re
from ble import BLE
from serial.tools.list_ports import comports
from utilities import *
from vibration_type import VibrationType


class Myo(object):

    def __init__(self):
        self.ble = None
        self.connection = None

    def connect(self, tty_port=None):
        self.safely_disconnect()
        self.find_bluetooth_adapter(tty_port)

        address = self.find_myo_device()
        print("address", address)
        connection_packet = self.ble.connect(address)
        self.connection = list(multiord(connection_packet.payload))[-1]
        print("self_connection", self.connection)
        self.ble.wait_event(3, 0)
        print('Connected.')

        is_fw_valid = self.valid_firmware_version()

        if is_fw_valid:
            device_name = self.read_attribute(0x03)
            print('Device name: %s' % device_name.payload[5:])
            # enable IMU data
            self.write_attribute(0x1d, b'\x01\x00')
            ## enable on/off arm notifications
            # self.write_attribute(0x24, b'\x02\x00')
            self.initialize()
        else:
            raise ValueError('The firmware version must be v1.x or greater.')

    def find_bluetooth_adapter(self, tty_port=None):
        if tty_port is None:
            tty_port = self.find_tty()
        if tty_port is None:
            raise ValueError('Bluetooth adapter not found!')

        self.ble = BLE(tty_port)

    def find_tty(self):
        return 'COM5'

    def run(self, timeout=None):
        if self.connection is not None:
            self.ble.receive_packet(timeout)
        else:
            raise ValueError('Myo device not paired.')

    def bytes_to_hex(self, byte_str):
        return ' '.join(format(ord(char), '02X') for char in byte_str)

    def valid_firmware_version(self):
        firmware = self.read_attribute(0x17)
        _, _, _, _, major, minor, patch, build = unpack('BHBBHHHH', firmware.payload.encode('latin-1'))

        print('Firmware version: %d.%d.%d.%d' % (major, minor, patch, build))

        return major > 0

    def add_listener(self, listener):
        if self.ble is not None:
            self.ble.add_listener(listener)
        else:
            print('Connect function must be called before adding a listener.')

    def vibrate(self, duration):
        cmd = b'\x03\x01'
        if duration == VibrationType.LONG:
            cmd = cmd + b'\x03'
        elif duration == VibrationType.MEDIUM:
            cmd = cmd + b'\x02'
        elif duration == VibrationType.SHORT:
            cmd = cmd + b'\x01'
        else:
            cmd = cmd + b'\x00'

        self.write_attribute(0x19, cmd)

    def initialize(self):
        #  to enable both raw data and	 pose notifications.
        # enable IMU data
        self.write_attribute(0x1d, b'\x01\x00')
        # enable EMG data
        self.write_attribute(0x28, b'\x01\x00')

        self.write_attribute(0x19, b'\x01\x03\x01\x01\x01')

    def find_myo_device(self):
        print('Find Myo device...')
        address = None
        self.ble.start_scan()
        while True:
            packet = self.ble.receive_packet()
            if packet.payload.endswith('\x06\x42\x48\x12\x4A\x7F\x2C\x48\x47\xB9\xDE\x04\xA9\x01\x00\x06\xD5'):
                address = list(multiord(packet.payload[2:8]))
                print(address)
                address1 = multiord(packet.payload[2:8])

                break

        self.ble.end_scan()
        return address

    def write_attribute(self, attribute, value):
        print("write_attribute")
        if self.connection is not None:
            self.ble.write_attribute(self.connection, attribute, value)

    def read_attribute(self, attribute):
        if self.connection is not None:
            return self.ble.read_attribute(self.connection, attribute)
        return None

    def safely_disconnect(self):
        if self.ble is not None:
            self.ble.end_scan()
            self.ble.disconnect(0)
            self.ble.disconnect(1)
            self.ble.disconnect(2)
            self.disconnect()

    def disconnect(self):
        if self.connection is not None:
            self.ble.disconnect(self.connection)
