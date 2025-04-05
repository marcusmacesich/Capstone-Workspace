import numpy as np
from Arm_Lib_New import Arm_Device1
import time
Arm = Arm_Device1()
time.sleep(.1)

#chess position definitions
h = -8.5
g = -5.8
f = -3.7
e = -1
d = 1.5
c = 4
b = 6.5
a = 9
row8 = 12.75
row7 = 15.5
row6 = 18.25
row5 = 21
row4 = 23.75
row3 = 26.5
row2 = 29
row1 = 32

# Chess Piece, close grip height, close grip width, transit width (off board)
# King - 7.2, 140, 140
# Queen - 7.2, 140, 140
# Rook - 6.2, 143, 143
# Bishop - 6.2, 143, 143
# Pawn - 5.5, 144, 144

# Move 1 - Black Queen - a6 -> f2 ---------------------------------------------------------

#user input position and color
row = row6
col = a
color = "black"
#arm will go home, open gripper, go to chess piece position, close gripper, raise chess piece, move to given cup, drop piece, return home

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)

#solve angles for chess piece position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 6.7)

#go to chess piece positon
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 30], 3000)
time.sleep(5)

#close gripper
Arm.Arm_serial_servo_write(6,140,500)
time.sleep(2)

#z hop
[x, y, z, ext] = Arm.get_pos_xyz()
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(x, y, z+15)
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 2000)
time.sleep(3)

# select drop space
row = row2
col = f

#solve angles for chess piece drop position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 8.7)

# move to drop space
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 3000)
time.sleep(5)

#open gripper to drop piece
Arm.Arm_serial_servo_write(6,100,500)
time.sleep(1)

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)

# Move 2 - White King - b2 -> g7 ---------------------------------------------------------

#user input position and color
row = row2
col = b
color = "white"
#arm will go home, open gripper, go to chess piece position, close gripper, raise chess piece, move to given cup, drop piece, return home

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)

#solve angles for chess piece position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 7.2)

#go to chess piece positon
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 30], 3000)
time.sleep(5)

#close gripper
Arm.Arm_serial_servo_write(6,140,500)
time.sleep(2)

#z hop
[x, y, z, ext] = Arm.get_pos_xyz()
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(x, y, z+15)
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 2000)
time.sleep(3)

# select drop space
row = row7
col = g

#solve angles for chess piece drop position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 7.7)

# move to drop space
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 3000)
time.sleep(5)

#open gripper to drop piece
Arm.Arm_serial_servo_write(6,100,500)
time.sleep(1)

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)

# Move 3 - White Bishop - h3 -> c5 ---------------------------------------------------------

#user input position and color
row = row3
col = h
color = "white"
#arm will go home, open gripper, go to chess piece position, close gripper, raise chess piece, move to given cup, drop piece, return home

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)

#solve angles for chess piece position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 6.2)

#go to chess piece positon
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 30], 3000)
time.sleep(5)

#close gripper
Arm.Arm_serial_servo_write(6,140,500)
time.sleep(2)

#z hop
[x, y, z, ext] = Arm.get_pos_xyz()
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(x, y, z+15)
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 2000)
time.sleep(3)

# select drop space
row = row5
col = c

#solve angles for chess piece drop position
[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 7.2)

# move to drop space
Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 140], 3000)
time.sleep(5)

#open gripper to drop piece
Arm.Arm_serial_servo_write(6,100,500)
time.sleep(1)

#go home - open gripper
Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 3000)
time.sleep(2)
