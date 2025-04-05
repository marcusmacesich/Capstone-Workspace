import numpy as np
from Arm_Lib_New import Arm_Device1
import time
Arm = Arm_Device1()
time.sleep(.1)

#send home 
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 89],4000)
time.sleep(5)

#read home angles
jointsAng = Arm.pos_array()
print(jointsAng)
#read servo home position coordinates
jointsPos = Arm.get_pos_xyz_proj(jointsAng)
print(jointsPos)
#send servos 2-4 independently to 0 and 180 deg and read position coordinates
#Send Servo 2 to 0 & 90 and read
Arm.Arm_serial_servo_write(2, 0, 4000)
time.sleep(5)

Serv2_0 = Arm.get_pos_xyz()
print(Serv2_0)
Arm.Arm_serial_servo_write(2, 90, 4000)
time.sleep(5)

Serv2_90 = Arm.get_pos_xyz()
print(Serv2_90)
#Reset
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 89],4000)
time.sleep(5)


#Send Servo 3 to 0 & 90 and read
Arm.Arm_serial_servo_write(3, 0, 4000)
time.sleep(5)

Serv3_0 = Arm.get_pos_xyz()
print(Serv3_0)
Arm.Arm_serial_servo_write(3, 90, 4000)
time.sleep(5)

Serv3_90 = Arm.get_pos_xyz()
print(Serv3_90)
#Reset
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 89],4000)
time.sleep(5)


#Send Servo 4 to 0 & 90 and read
Arm.Arm_serial_servo_write(4, 0, 4000)
time.sleep(5)

Serv4_0 = Arm.get_pos_xyz()
print(Serv4_0)
Arm.Arm_serial_servo_write(4, 90, 4000)
time.sleep(5)

Serv4_90 = Arm.get_pos_xyz()
print(Serv4_90)
#Reset
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 89],4000)
time.sleep(5)


#send servo 4 to 0 and 90 deg and and read position coordinates
Arm.Arm_serial_servo_write(4, 90, 4000)
time.sleep(5)

print(Arm.get_pos_xyz())
#send servo 1 to 0 and 180 deg and read position coordinates
Arm.Arm_serial_servo_write(1, 179, 4000)
time.sleep(5)
Arm.Arm_serial_servo_write(4, 0, 4000)
print(Arm.get_pos_xyz())
time.sleep(5)

print(Arm.get_pos_xyz())
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 89],4000)
