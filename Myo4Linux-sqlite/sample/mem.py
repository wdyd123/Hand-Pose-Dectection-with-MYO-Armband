import serial.tools.list_ports

# 获取所有串口
ports = serial.tools.list_ports.comports()

# 打印所有串口信息
for port in ports:
    print(f"串口名称: {port.device}, 描述: {port.description}")
