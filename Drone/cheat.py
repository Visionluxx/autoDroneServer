import time
import serial
import struct

# =====================
# MSP CORE FUNCTIONS
# =====================
def checksum(data: bytes) -> int:
    s = 0
    for b in data:
        s ^= b
    return s

def send_msp(ser: serial.Serial, cmd: int, payload: bytes = b'') -> None:
    header = b'$M<'
    size = len(payload)
    packet = bytearray([size, cmd]) + payload
    crc = checksum(packet)
    ser.write(header + packet + bytes([crc]))

def send_rc(ser: serial.Serial,
            roll=1500, pitch=1500, throttle=1500, yaw=1500,
            aux1=1000, aux2=1000, aux3=1000, aux4=1000):
    """Gửi giá trị RC channel (1000–2000) tới FC."""
    channels = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    payload = b''.join(struct.pack('<H', ch) for ch in channels)
    send_msp(ser, 200, payload)  # 200 = MSP_SET_RAW_RC


# =====================
# CHỨC NĂNG BAY
# =====================
def maintain_rc(ser, duration, **kwargs):
    """Duy trì giá trị RC trong một khoảng thời gian (giữ ổn định tín hiệu)."""
    start = time.time()
    while time.time() - start < duration:
        send_rc(ser, **kwargs)
        time.sleep(0.02)  # 50 Hz

def hover(ser, duration=2.0):
    print("🟡 Hovering...")
    maintain_rc(ser, duration, roll=1500, pitch=1500, yaw=1500, throttle=1500)

def up(ser, duration=2.0, throttle=1700):
    print("🛫 Bay lên...")
    maintain_rc(ser, duration, throttle=throttle)

def forward(ser, duration=2.0, pitch=1600):
    print("⬆️  Bay thẳng...")
    maintain_rc(ser, duration, pitch=pitch)

def right(ser, duration=2.0, roll=1600):
    print("➡️  Nghiêng phải...")
    maintain_rc(ser, duration, roll=roll)

def left(ser, duration=2.0, roll=1400):
    print("⬅️  Nghiêng trái...")
    maintain_rc(ser, duration, roll=roll)

def down(ser, duration=2.0, throttle=1200):
    print("🛬 Hạ xuống...")
    maintain_rc(ser, duration, throttle=throttle)


# =====================
# BAY TỰ ĐỘNG
# =====================
def autonomous_flight(ser):
    """Chuỗi hành động bay tự động."""
    hover(ser, 1.5)        # Chuẩn bị, giữ ổn định
    up(ser, 2.0)           # Bay lên
    hover(ser, 1.0)        # Dừng lại
    forward(ser, 2.0)      # Bay thẳng 1 đoạn
    right(ser, 1.5)        # Nghiêng phải
    forward(ser, 2.0)      # Bay thẳng 1 đoạn
    left(ser, 1.5)         # Nghiêng trái
    forward(ser, 2.0)      # Bay thẳng 1 đoạn
    down(ser, 2.0)         # Hạ xuống
    hover(ser, 1.0)        # Đứng yên
    print("✅ Hoàn thành bài bay tự động")


# =====================
# CHẠY CHƯƠNG TRÌNH
# =====================
if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
    time.sleep(2)
    print("🔗 Đã kết nối với FC")
    
    autonomous_flight(ser)
    
    ser.close()
