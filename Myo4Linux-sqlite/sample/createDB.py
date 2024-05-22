import sys
import sqlite3
def main():
 


    conn = sqlite3.connect('myo.db');
    print ("Opened database successfully");
    c = conn.cursor();
    c.execute('''CREATE TABLE EMG
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       POD0           INTEGER  NOT NULL,
       POD1           INTEGER      NOT NULL,
       POD2           INTEGER      NOT NULL,
       POD3           INTEGER      NOT NULL,
       POD4           INTEGER      NOT NULL,
       POD5           INTEGER      NOT NULL,
       POD6           INTEGER      NOT NULL,
       POD7           INTEGER      NOT NULL);''')
    print ("Table EMG created successfully");
    c.execute('''CREATE TABLE IMU
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       QUAT0           INTEGER  NOT NULL,
       QUAT1           INTEGER      NOT NULL,
       QUAT2           INTEGER      NOT NULL,
       QUAT3           INTEGER      NOT NULL,
       ACC0           INTEGER      NOT NULL,
       ACC1           INTEGER      NOT NULL,
       ACC2           INTEGER      NOT NULL,
       GYRO0           INTEGER      NOT NULL,
       GYRO1           INTEGER      NOT NULL,
       GYRO2           INTEGER      NOT NULL,
       LABEL           INTEGER      NOT NULL);''')
    print ("Table IMU created successfully");
    conn.commit();
    conn.close();
if __name__ == '__main__':
    main()