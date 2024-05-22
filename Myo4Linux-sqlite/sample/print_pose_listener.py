import sys
import time
from datetime import   date,datetime
import sqlite3
sys.path.append('../lib/')

from device_listener import DeviceListener
from pose_type import PoseType

class PrintPoseListener(DeviceListener):
    global conn
    conn = sqlite3.connect('myo.db')
    global c
    c = conn.cursor()

    def on_emg(self, emg):
        print("EMG:")
        print(emg)

        try:
            c.execute("INSERT INTO EMG (POD0,POD1,POD2,POD3,POD4,POD5,POD6,POD7) VALUES (?,?,?,?,?,?,?,?)",(int(emg[0]),int(emg[1]),int(emg[2]),int(emg[3]),int(emg[4]),int(emg[5]),int(emg[6]),int(emg[7])))
            conn.commit()
            print("EMG data inserted successfully!")
        except sqlite3.Error as e:
            print("Failed to insert EMG data:", e)

        time.sleep(0)

    def on_imu(self, quat, acc, gyro):
        print("IMU:")
        print(quat)
        print(acc)
        print(gyro)

        try:
            c.execute("INSERT INTO IMU (QUAT0,QUAT1,QUAT2,QUAT3,ACC0,ACC1,ACC2,GYRO0,GYRO1,GYRO2,LABEL) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(int(quat[0]),int(quat[1]),int(quat[2]),int(quat[3]),int(acc[0]),int(acc[1]),int(acc[2]),int(gyro[0]),int(gyro[1]),int(gyro[2]),int(PoseType.REST)))
            conn.commit()
            print("IMU data inserted successfully!")
        except sqlite3.Error as e:
            print("Failed to insert IMU data:", e)

        time.sleep(0)



