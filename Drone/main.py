import serial
import struct

# =====================
# MSP CORE FUNCTIONS
# =====================
def checksum(data: bytes) -> int:
    """Tính checksum bằng XOR cho gói MSP."""
    s = 0
    for b in data:
        s ^= b
    return s

def send_msp(ser: serial.Serial, cmd: int, payload: bytes = b'') -> None:
    """Gửi gói MSP tới Flight Controller."""
    header = b'$M<'
    size = len(payload)
    packet = bytearray([size, cmd]) + payload
    crc = checksum(packet)
    ser.write(header + packet + bytes([crc]))

def read_msp(ser: serial.Serial, cmd: int):
    """Gửi request và đọc phản hồi từ FC."""
    send_msp(ser, cmd)
    header = ser.read(3)  # chờ '$M>'
    if not header.startswith(b'$M>'):
        return None
    size = ser.read(1)[0]
    cmd_res = ser.read(1)[0]
    data = ser.read(size)
    crc = ser.read(1)[0]
    return data if cmd_res == cmd else None


# =====================
# CONTROL FUNCTIONS
# =====================
def send_rc(ser: serial.Serial, roll=1500, pitch=1500, throttle=1000, yaw=1500, aux1=1000, aux2=1000, aux3=1000, aux4=1000):
    """Gửi giá trị RC channel (1000–2000) tới FC."""
    channels = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    payload = b''.join(struct.pack('<H', ch) for ch in channels)
    send_msp(ser, 200, payload)  # 200 = MSP_SET_RAW_RC


def forward(ser: serial.Serial, speed=100):
    """Bay tiến: tăng pitch."""
    send_rc(ser, pitch=1500 + speed)

def backward(ser: serial.Serial, speed=100):
    """Bay lùi: giảm pitch."""
    send_rc(ser, pitch=1500 - speed)

def left(ser: serial.Serial, speed=100):
    """Nghiêng trái: giảm roll."""
    send_rc(ser, roll=1500 - speed)

def right(ser: serial.Serial, speed=100):
    """Nghiêng phải: tăng roll."""
    send_rc(ser, roll=1500 + speed)

def yaw_left(ser: serial.Serial, speed=100):
    """Xoay trái: giảm yaw."""
    send_rc(ser, yaw=1500 - speed)

def yaw_right(ser: serial.Serial, speed=100):
    """Xoay phải: tăng yaw."""
    send_rc(ser, yaw=1500 + speed)

def up(ser: serial.Serial, throttle=1700):
    """Tăng độ cao."""
    send_rc(ser, throttle=throttle)

def down(ser: serial.Serial, throttle=1200):
    """Giảm độ cao."""
    send_rc(ser, throttle=throttle)


# =====================
# SENSOR FUNCTIONS
# =====================
def get_attitude(ser: serial.Serial):
    """
    Đọc attitude (roll, pitch, yaw) từ FC.
    Roll/Pitch: 0.1 độ, Yaw: 1 độ.
    """
    data = read_msp(ser, 108)  # 108 = MSP_ATTITUDE
    if data:
        roll, pitch, yaw = struct.unpack('<hhh', data)
        return roll / 10.0, pitch / 10.0, yaw
    return None

def get_heading(ser: serial.Serial):
    """
    Lấy hướng drone (la bàn).
    - Dựa trên yaw từ MSP_ATTITUDE.
    - Trả về giá trị 0–360 độ.
    """
    attitude = get_attitude(ser)
    if attitude:
        _, _, yaw = attitude
        heading = yaw % 360
        return heading
    return None


def main (cam, link, ser):
  fromm .camera import capture
  capture (cam)
  a = os.system (f'curl -X POST -F "image=..." {link}')
  if a:
    pass
  send_rc (ser)



# Mở cổng serial tới FC
ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
	
#receive link
import os
link=input("link")
link = link + "upload"

#connect camera
from .camera import connect_cam
cam = connect_cam()
			
#main thread
while True:
	import threading
	import time
	import sys
	from .flying import main

	t = threading.Thread(target=main, args = (cam, link, ser))
	t.start()

	t.join(timeout=5)  # Chờ tối đa 5 giây
	if t.is_alive():
		print("Quá 5 giây, dừng chương trình")
		sys.exit()
		break

down (ser)
		

#release cam
cam.release()
