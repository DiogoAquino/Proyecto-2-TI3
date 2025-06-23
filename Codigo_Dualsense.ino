from pydualsense import *
import serial
import time

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

ds = DualSense()
ds.init()

print("Controlando servos con el joystick izquierdo...")

try:
while True:
x = ds.leftX
y = ds.leftY

    servo1 = int((x + 127) * 180 / 254)
    servo2 = int((y + 127) * 180 / 254)

    data = f"{servo1},{servo2}\n"
    arduino.write(data.encode())
    time.sleep(0.05)
except KeyboardInterrupt:
ds.close()
arduino.close()
