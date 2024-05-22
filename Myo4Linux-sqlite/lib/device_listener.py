from utilities import *


class DeviceListener(object):
    def handle_data(self, data):
        print("handel data cls,cmd", data.cls, data.command)
        if data.cls != 4 and data.command != 5:
            return

        connection, attribute, data_type = unpack('BHB', data.payload[:4].encode('latin-1'))
        payload = data.payload[5:]

        if attribute == 0x27:
            vals = unpack('8HB', payload.encode('latin-1'))
            emg = vals[:8]
            moving = vals[8]
            self.on_emg(emg)

        elif attribute == 0x1c:
            vals = unpack('10h', payload.encode('latin-1'))
            quat = vals[:4]
            acc = vals[4:7]
            gyro = vals[7:10]
            self.on_imu(quat, acc, gyro)

    def on_pose(self, value):
        pass

    def on_emg(self, emg, moving):
        pass

    def on_imu(self, quat, acc, gyro):
        pass
