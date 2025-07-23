from pca9685 import PCA9685
# from picocat import Servos
from machine import I2C, Pin
from servo import Servos
from mpu6500 import MPU6500, SF_G, SF_DEG_S
import time


sda = Pin(21)
scl = Pin(22)
i2c = I2C(sda=sda, scl=scl)

pca = PCA9685(i2c=i2c)
servo = Servos(i2c=i2c)
sensor = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)

"""
Servo index 0 is X
Servo index 1 is Y
Servo index 2 is Z

"""

def map_to_servo_degrees(accel_tuple):
    # Map each axis (x, y, z) from -1 to 1 to 0 to 180 degrees
    x, y, z = accel_tuple
    
    # Map to 0-180 range instead of 0-90
    x_servo = int(((x + 1) / 2) * 180)  # Clamps to 0-180 range
    y_servo = int(((y + 1) / 2) * 180)  # Clamps to 0-180 range
    z_servo = int(((z + 1) / 2) * 180)  # Clamps to 0-180 range
    
    # Ensure the values are within the 0 to 180 range (just in case)
    x_servo = max(0, min(180, x_servo))
    y_servo = max(0, min(180, y_servo))
    z_servo = max(0, min(180, z_servo))
    
    return x_servo, y_servo, z_servo


servo.position(index=0, degrees=90)
servo.position(index=1, degrees=90)
servo.position(index=2, degrees=90)

while True:
    time.sleep(.1)
    servo_positions = map_to_servo_degrees(sensor.acceleration)
    print(servo_positions) 
    servo.position(index=0, degrees=servo_positions[0])
    servo.position(index=1, degrees=servo_positions[1])
    servo.position(index=2, degrees=servo_positions[2])
    
		