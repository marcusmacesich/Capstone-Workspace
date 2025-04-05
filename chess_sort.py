import numpy as np
from Arm_Lib_New import Arm_Device1
import time
Arm = Arm_Device1()
time.sleep(.1)

#chess position definitions
h = -8.5
g = -6
f = -3.5
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
row2 = 29.25
row1 = 32

def chess_sort(row, col, color):
	#arm will go home, open gripper, go to chess piece position, close gripper, raise chess piece, move to given cup, drop piece, return home

	#go home - open gripper
	Arm.Arm_serial_servo_write6_array([90,90,90,90,90,30], 2000)
	time.sleep(2)

	#solve angles for chess piece position
	[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(row, col, 5.2)

	#go to chess piece positon
	Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 30], 2000)
	time.sleep(2)


	#close gripper
	Arm.Arm_serial_servo_write(6,135,500)
	time.sleep(1)

	#z hop
	[x, y, z, ext] = Arm.get_pos_xyz()
	[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(x, y, z+15)
	Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 135], 2000)
	time.sleep(2)

	#go to cup corresponding to color
	if color == "black":
   		 [theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(0,10,4.2)
	if color == "white":
    		[theta1, theta2, theta3, theta4] = Arm.calc_theor_angles(0,-10,4.2)
	Arm.Arm_serial_servo_write6_array([theta1, theta2, theta3, theta4, 90, 135], 2000)
	time.sleep(2)

	#open gripper to drop piece
	Arm.Arm_serial_servo_write(6,100,500)
	time.sleep(2)
	Arm.Arm_serial_servo_write6_array([theta1, 90, 90, 90, 90, 100], 2000)
	time.sleep(1)
		

chess_sort(row8,h,"black")
chess_sort(row5, e, "white")
chess_sort(row3, b, "black")
chess_sort(row1, f, "white")
chess_sort(row7, b, "white") 
Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 30], 2000)












