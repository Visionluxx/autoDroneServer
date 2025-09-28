# Hàm tính checksum MSP để kiểm tra độ toàn vẹn dữ liệu 
def checksum(data):
    s = 0
    for b in data:
        s ^= b
    return s

# Hàm gửi MSP packet
def send_msp(cmd, payload=b''):
    header = b'$M<'
    size = len(payload)
    packet = bytearray([size, cmd]) + payload
    crc = checksum(packet)
    ser.write(header + packet + bytes([crc]))

# Hàm gửi RC (roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4)
# giá trị 1000–2000 (giống RC channel)
def send_rc(roll, pitch, throttle, yaw, aux1=1000, aux2=1000, aux3=1000, aux4=1000):
    channels = [roll, pitch, throttle, yaw, aux1, aux2, aux3, aux4]
    payload = b''.join(struct.pack('<H', ch) for ch in channels)
    send_msp(200, payload)  # 200 = MSP_SET_RAW_RC
