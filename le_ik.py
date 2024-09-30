import xarm
import math
import time
import numpy as np

# This program is incomplete and needs to be fully tested & debugged.
# Offsets were introduced to compensate for strange servo behavior of the LeArm
# For this to work, the xarm library must be modified to change the limit from 1250 to 2900 on servo commands
# If you have the .venv folder, first run '.venv/Scripts/activate' from a console in the project directory
# Run the program with 'python le_ik.py'

# Declare arm HID serial object
arm = xarm.Controller('USB', debug=True)

# Link lengths (in centimeters)
L1 = 1.27  # Base height to shoulder joint
L2 = 10.16  # Shoulder to elbow joint
L3 = 10.16  # Elbow to wrist joint
L4 = 17.78   # Wrist joint to end-effector

# Joint limits in degrees
joint_limits = {
    'theta1': (-90.1, 90.1),  # Base rotation
    'theta2': (-90.1, 90.1),  # Shoulder
    'theta3': (-90.1, 90.1),  # Elbow
    'theta4': (-90.1, 90.1),  # Wrist pitch
    'theta5': (-90.1, 90.1),  # Wrist yaw
    #'theta6': (-90.1, 90.1),  # Jaw closed
}


# Servo offsets and directions
servo_offsets = {
    'theta1': 0.0,
    'theta2': 0.0,
    'theta3': 0.0,
    'theta4': 90.0,
    'theta5': 0.0,
    #'theta6': 0.0, 
}

servo_directions = {
    'theta1': 1,
    'theta2': -1,
    'theta3': -1,
    'theta4': -1,
    'theta5': 1,
    #'theta6': 1,
}

# Servo definitions
claw = xarm.Servo(1)           # Claw
rot = xarm.Servo(2)            # Wrist rotation (theta5)
wrist = xarm.Servo(3)          # Wrist pitch (theta4)
elbow = xarm.Servo(4)          # Elbow (theta3)
shoulder = xarm.Servo(5)       # Shoulder (theta2)
base = xarm.Servo(6)           # Base rotation (theta1)

# Function to calculate robot joint angles from desired position in 3D space
def inverse_kinematics(x_e, y_e, z_e, roll=0.0, pitch=0.0, yaw=0.0):

    # Convert orientation angles from degrees to radians
    roll_rad = math.radians(roll)
    pitch_rad = math.radians(pitch)
    yaw_rad = math.radians(yaw)

    # Adjust for base neutral position at 45 degrees
    theta1_rad = math.atan2(y_e, x_e) # - math.radians(45.0)
    theta1 = math.degrees(theta1_rad) - 45.0

    # Ensure theta1 is within joint limits
    if not within_limits(theta1, 'theta1'):
        print("Theta1 out of limits")
        return None

    # Distance from base to projection of the end-effector in XY plane
    r = math.hypot(x_e, y_e)

    #adjusted_pitch_rad = math.radians(pitch + 90)

    # Compute the position of the wrist center
    x_w = x_e - L4 * math.cos(pitch_rad) * math.cos(yaw_rad)
    y_w = y_e - L4 * math.cos(pitch_rad) * math.sin(yaw_rad)
    z_w = z_e - L4 * math.sin(pitch_rad)  # Subtract along Z-axis

    # Compute wrist center distances
    r_wrist = math.hypot(x_w, y_w)
    s = z_w - L1

    # Compute D
    D = (r_wrist**2 + s**2 - L2**2 - L3**2) / (2 * L2 * L3)

    # Clamp D to the valid range [-1.0, 1.0]
    D = max(min(D, 1.0), -1.0)

    # Possible elbow angles
    theta3_rad = math.atan2(-math.sqrt(1 - D**2), D)  # Elbow down solution
    theta3 = math.degrees(theta3_rad)

    # Compute shoulder angle
    k1 = L2 + L3 * math.cos(theta3_rad)
    k2 = L3 * math.sin(theta3_rad)
    theta2_rad = math.atan2(s, r_wrist) - math.atan2(k2, k1)
    theta2 = math.degrees(theta2_rad) - 90

    # Adjust for joint directions
    theta2 = theta2
    theta3 = -theta3  # Elbow joint moves opposite

    # Compute wrist orientation angles
    theta4 = pitch - theta2 + theta3  # Adjusted wrist pitch angle
    print(pitch, theta2, theta3)
    theta5 = roll  # Wrist rotation aligns with end-effector roll

    # Normalize joint angles within limits
    joint_angles = {
        'theta1': normalize_angle(theta1, 'theta1'),
        'theta2': normalize_angle(theta2, 'theta2'),
        'theta3': normalize_angle(theta3, 'theta3'),
        'theta4': normalize_angle(theta4, 'theta4'),
        'theta5': normalize_angle(theta5, 'theta5'),
    }

    return joint_angles


# Checks that angles are within joint limits
def within_limits(angle, joint_name):
    min_limit, max_limit = joint_limits[joint_name]
    return min_limit <= angle <= max_limit

# Rounds angles within joint limits
def normalize_angle(angle, joint_name):
    min_limit, max_limit = joint_limits[joint_name]
    angle = max(min(angle, max_limit), min_limit)
    return angle

def rotation_matrix_0_3(theta1, theta2, theta3):
    """
    Computes the rotation matrix from base to wrist (frame 3).
    """
    R0_1 = np.array([
        [math.cos(theta1), -math.sin(theta1), 0],
        [math.sin(theta1),  math.cos(theta1), 0],
        [0,                0,                1],
    ])
    R1_2 = np.array([
        [math.cos(theta2), -math.sin(theta2), 0],
        [0,                0,               -1],
        [math.sin(theta2),  math.cos(theta2), 0],
    ])
    R2_3 = np.array([
        [math.cos(theta3), -math.sin(theta3), 0],
        [0,                0,                1],
        [-math.sin(theta3), -math.cos(theta3), 0],
    ])
    R0_3 = np.matmul(R0_1, np.matmul(R1_2, R2_3))
    return R0_3

def euler_angles_to_rotation_matrix(roll, pitch, yaw):
    """
    Converts roll, pitch, yaw angles to a rotation matrix.
    """
    R_roll = np.array([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll),  math.cos(roll)],
    ])
    R_pitch = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)],
    ])
    R_yaw = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw),  math.cos(yaw), 0],
        [0, 0, 1],
    ])
    R = np.matmul(R_yaw, np.matmul(R_pitch, R_roll))
    return R

# Uses inverse kinematics function to move the robot to desired 3D parameters
def move_to_position(x_d,y_d,z_d,roll_d,pitch_d,yaw_d):

    # Compute joint angles for desired position with inverse kinematics
    joint_angles = inverse_kinematics(x_d,y_d,z_d,roll_d,pitch_d,yaw_d)

    # Print calculated angles
    print("Calculated Angles:")
    print(joint_angles)

    # Check if a valid solution was returned
    if joint_angles is None:
        print("Could not calculate joint angles for the destination.")
    else:
        # Map joint angles to servo angles with offsets and directions
        servo_angles={}
        for joint, angle in joint_angles.items():
            servo_angle = servo_offsets[joint] + servo_directions[joint] * angle
            servo_angles[joint] = servo_angle

        # Print actual angles the servos are commanded
        print("Servo angles:")
        print(servo_angles)

        # Update each servo with its offset angle
        base.angle = servo_angles['theta1']
        shoulder.angle = servo_angles['theta2']
        elbow.angle = servo_angles['theta3']
        wrist.angle = servo_angles['theta4']
        rot.angle = servo_angles['theta5']

        # Move arm into calculated position
        arm.setPosition([base, shoulder, elbow, wrist, rot], wait=True)

# Arm to completely vertical position
move_to_position(0.0,0.0,L1 + L2 + L3 + L4,0.0,90.0,0.0)

time.sleep(1)

# Arm horizontal to ground on x axis
move_to_position(L2 + L3 + L4, 0.0, L1, 0.0, 0.0, 0.0)

time.sleep(1)

# Arm to completely vertical position
move_to_position(0.0,0.0,L1 + L2 + L3 + L4,0.0,90.0,0.0)

time.sleep(1)

# Arm horizontal to ground on y axis
move_to_position(0.0, L2 + L3 + L4, L1, 0.0, 0.0, 0.0)

time.sleep(1)

# Arm to completely vertical position
move_to_position(0.0,0.0,L1 + L2 + L3 + L4,0.0,90.0,0.0)

time.sleep(1)

# Shoulder up, elbow at right angle on y axis
move_to_position(0.0,L3 + L4, L1 + L2, 0.0, 0.0, 90.0)

time.sleep(1)

# Arm to completely vertical position
move_to_position(0.0,0.0,L1 + L2 + L3 + L4,0.0,90.0,0.0)

time.sleep(1)

# Shoulder up, elbow at right angle on x axis
move_to_position(L3 + L4, 0.0, L1 + L2, 0.0, 0.0, 0.0)