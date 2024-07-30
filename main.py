# enable_firefly
# code make you sleepy
# https://makex.ckl.moe/lol
import novapi
from mbuild import power_manage_module
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.smart_camera import smart_camera_class
from mbuild.led_matrix import led_matrix_class
from mbuild.button import button_class
import mbuild
import time
import math

# Control System Config
Speed_Modifier = 250
Speed_Modifier2 = 1.2
TURN_SPEED_MODIFIER = 1.5
CTLMODE = 2
DC_LOCK_V = 6

FEEDER_POWER = 50
# FEEDER_POWER = 80

# Automatic Stage Config
ENABLE_AUTO = True
V_AUTO_STAGE = 0
AUTO_RPM = 250
AUTO_SLIDE_RPM = 80
NEG_AUTO_RPM = -200

#AUTO CAM CONFIG
MIN_X_POS = 130
MAX_X_POS = 175

AUTO_SIDE = None

SPIN_TIG = False

SPINNER_PORT = "DC7"

# stuff
FR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
BR_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
FL_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")

# Servos
BRUSHLESS_SERVO = smartservo_class("M5", "INDEX1")
BUTTOM_GRIPPER = smartservo_class("M5", "INDEX2")
GRIPPER_ANGLE = smartservo_class("M5", "INDEX3")

# Ranging
LEFT_RANGING = ranging_sensor_class("PORT5", "INDEX1")
BACK_RANGING = ranging_sensor_class("PORT5", "INDEX2")
RIGHT_RANGING = ranging_sensor_class("PORT5", "INDEX3")
FRONT_L_RANGING = ranging_sensor_class("PORT5", "INDEX5")
FRONT_R_RANGING = ranging_sensor_class("PORT5", "INDEX4")

# Gripper
GRIPPER_RANGING = ranging_sensor_class("PORT4", "INDEX1")

# Debugging Hardware
debug = led_matrix_class("PORT4", "INDEX1")
button_1 = button_class("PORT4", "INDEX1")

# Cameras
# FRONT_TOP_CAM = smart_camera_class("PORT4", "INDEX1")

def Motor_Control(M1, M2, M3, M4):
    FR_ENCODE_M1.set_power(M1)
    BR_ENCODE_M2.set_power(M2)
    FL_ENCODE_M3.set_power(M3)
    BL_ENCODE_M4.set_power(M4)

def Motor_RPM(M1, M2, M3, M4):
    FR_ENCODE_M1.set_speed(M1)
    BR_ENCODE_M2.set_speed(M2)
    FL_ENCODE_M3.set_speed(M3)
    BL_ENCODE_M4.set_speed(M4)

def Move_FB(rpm):
    """Move Forward and Backward (+rpm for Forward, -rpm for Backward)"""
    Motor_RPM(rpm, rpm, rpm * -1, rpm * -1)

def Move_LR(rpm):
    """Move Side Left and Right (+rpm for Left, -rpm for Right)"""
    Motor_RPM(rpm*-1, rpm, rpm*-1, rpm)

def Move_Diag(direction, rpm):
    """
    Moves the robot diagonally in the specified direction.  
    FL, FR, BL, BR  
    """

    if direction == "FL":
        Motor_RPM(0, rpm, -rpm, 0)
    elif direction == "FR":
       Motor_RPM(rpm, 0, 0, -rpm)
    elif direction == "BL":
       Motor_RPM(-rpm, 0, 0, rpm)
    elif direction == "BR":
        Motor_RPM(0, -rpm, rpm, 0)
    else:
        Motor_RPM(0,0,0,0)

def Move_Turn(rpm):
    """Turn Left or Right (+rpm for Left, -rpm for Right)"""
    Motor_RPM(rpm, rpm, rpm, rpm)

# def Auto_Maintain_Grip(t_distance=16):
def Auto_Maintain_Grip(t_distance=15):
    distance = GRIPPER_RANGING.get_distance()  # Get current distance

    # Calculate power based on distance from target, ensuring a minimum of 10
    power = max(10, abs(distance - t_distance) * 4)

    if distance > t_distance:
        power_expand_board.set_power("DC4", power)  # Close gripper
    elif distance < t_distance:
        power_expand_board.set_power("DC4", -power)  # Open gripper
    else:
        power_expand_board.set_power("DC4", DC_LOCK_V)  # Maintain grip

def is_within_range(number, target, margin=5):
    return target - margin <= number <= target + margin

def Auto_Turn(degree:int):
    """Turn Left or Right (+degree for Left, -degree for Right)"""
    target_angle = novapi.get_yaw() + degree
    if target_angle > novapi.get_yaw():
        while novapi.get_yaw() < target_angle :
            Auto_Maintain_Grip()
            Move_Turn(-100) 
    elif target_angle < novapi.get_yaw():
        while novapi.get_yaw() > target_angle :
            Auto_Maintain_Grip()
            Move_Turn(100)
    Motor_RPM(0, 0, 0, 0)

def No_Drift():
    """run the nodrift code and sends back weather or not the code is executed"""
    # Mango's NoDrift(tm) V3
    if abs(FRONT_L_RANGING.get_distance() - FRONT_R_RANGING.get_distance()) > 3 and not ((FRONT_L_RANGING.get_distance() == 200) and (FRONT_R_RANGING.get_distance() == 200)):
        if FRONT_L_RANGING.get_distance() > FRONT_R_RANGING.get_distance():
            Move_Turn(50)
        else:
            Move_Turn(-50)
        return False
    else:
        return True
    
def Auto_stage_new_1():
    """new spinner auto"""
    global ENABLE_AUTO, V_AUTO_STAGE, AUTO_SIDE
    while power_manage_module.is_auto_mode():
        debug.show('A' + str(str(AUTO_SIDE) + str(V_AUTO_STAGE)), wait=False)

        Auto_Maintain_Grip()

        if V_AUTO_STAGE == 0:
            power_expand_board.set_power(SPINNER_PORT, -100)
            Move_FB(250)
            while FRONT_L_RANGING.get_distance() > 20:
                time.sleep(0.001)
                Auto_Maintain_Grip()
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            
        elif V_AUTO_STAGE == 1:
            power_expand_board.set_power(SPINNER_PORT, -100)
            if FRONT_L_RANGING.get_distance() > 8:
                Move_FB(100)
            elif No_Drift():
                if AUTO_SIDE == "R": 
                    if LEFT_RANGING.get_distance() < 20:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(-90, 120, -90, 120)
                else:
                    if RIGHT_RANGING.get_distance() < 20:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(130, -90, 130, -90)

        elif V_AUTO_STAGE == 2:
            Move_FB(0)
            Auto_Maintain_Grip()
            power_expand_board.set_power(SPINNER_PORT, 0)
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            continue

        time.sleep(0.001)

def Auto_stage_new_2():
    """new spinner auto for co-op"""
    global ENABLE_AUTO, V_AUTO_STAGE, AUTO_SIDE
    while power_manage_module.is_auto_mode():
        debug.show('A' + str(str(AUTO_SIDE) + str(V_AUTO_STAGE)), wait=False)

        Auto_Maintain_Grip()

        if V_AUTO_STAGE == 0:
            # if AUTO_SIDE == "L":
            #     Auto_Turn(0.01)
            # else:
            #     Auto_Turn(-0.01)
            V_AUTO_STAGE = V_AUTO_STAGE + 1
        if V_AUTO_STAGE == 1:
            power_expand_board.set_power(SPINNER_PORT, -100)
            Move_FB(250)
            while FRONT_L_RANGING.get_distance() > 20:
                time.sleep(0.001)
                Auto_Maintain_Grip()
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            
        elif V_AUTO_STAGE == 2:
            power_expand_board.set_power(SPINNER_PORT, -100)
            if FRONT_L_RANGING.get_distance() > 8:
                Move_FB(100)
                # if AUTO_SIDE == "L":
                #     Move_Diag("FL", 200)
                # else:
                #     Move_Diag("FR", 200)
            elif No_Drift():
                if AUTO_SIDE == "R": 
                    if LEFT_RANGING.get_distance() < 30:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(-90, 120, -90, 120)
                else:
                    if RIGHT_RANGING.get_distance() < 30:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(130, -90, 130, -90)

        elif V_AUTO_STAGE == 3:
            Move_FB(0)
            Auto_Maintain_Grip()
            power_expand_board.set_power(SPINNER_PORT, 0)
            Move_FB(-250)
            time.sleep(0.5)
            Move_FB(0)
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            continue

        time.sleep(0.001)

## END
## END
## END

def Movement(flip=1):
    LX = gamepad.get_joystick("Lx") * flip
    LY = gamepad.get_joystick("Ly") * flip
    RX = gamepad.get_joystick("Rx")

    if abs(LX) > 10 or abs(LY) > 10:
        left_angle = math.atan2(-LY, LX)
        cross_left_power = math.sin(left_angle + (1/4 * math.pi)) * Speed_Modifier
        cross_right_power = math.sin(left_angle - (1/4 * math.pi)) * Speed_Modifier
        Motor_RPM(cross_right_power, -cross_left_power, cross_left_power, -cross_right_power)
    elif abs(RX) > 10:
        TURN_SPEED = RX * TURN_SPEED_MODIFIER
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

# Button map for keymap 1, controls shooting system
def S1_Keymap():
    # main loading system controls
    if gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC1", 100)
        power_expand_board.set_power("DC2", 100)
    elif gamepad.is_key_pressed("Right"):
        power_expand_board.set_power("DC2", -100)
    elif gamepad.is_key_pressed("Left"):
        power_expand_board.set_power("DC1", -100)
    elif gamepad.is_key_pressed("L1") or gamepad.is_key_pressed("Up"):
        power_expand_board.set_power("DC1", 0)
        power_expand_board.set_power("DC2", 0)

    # conveyor control
    if gamepad.is_key_pressed("N2"):
        power_expand_board.set_power("DC3", FEEDER_POWER)
    elif gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("DC3", FEEDER_POWER * -1)
    else:
        power_expand_board.set_power("DC3", 0)

    # Shooter Control
    if gamepad.is_key_pressed("N4"):
        power_expand_board.set_power("BL1", 100)
        power_expand_board.set_power("BL2", 100)
    elif gamepad.is_key_pressed("R1"):
        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")

    # Brushless Angle
    if gamepad.is_key_pressed("+"):
        BRUSHLESS_SERVO.move_to(-23, 100)
        # FEEDER_POWER = 80
        # BRUSHLESS_SERVO.move(1, 50)
    elif gamepad.is_key_pressed("≡"):
        BRUSHLESS_SERVO.move_to(-5, 100)
        # FEEDER_POWER = 50
        # BRUSHLESS_SERVO.move(-1, 50)

    if gamepad.is_key_pressed("R_Thumb"):
        power_expand_board.set_power("DC2", 100)
        power_expand_board.set_power("DC1", 0)
    elif gamepad.is_key_pressed("L2"):
        power_expand_board.set_power("DC1", 0)

# Button map for keymap 2, controls main gripper
def S2_Keymap ():
    global SPIN_TIG
    if SPIN_TIG:
        Auto_Maintain_Grip()
        if gamepad.is_key_pressed("≡"):
            SPIN_TIG = False
            power_expand_board.set_power(SPINNER_PORT, 0)
    else:
        if gamepad.is_key_pressed("N1"):
            power_expand_board.set_power(SPINNER_PORT, 100)
        elif gamepad.is_key_pressed("N4"):
            power_expand_board.set_power(SPINNER_PORT, -100)
        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power(SPINNER_PORT, 100)
        elif gamepad.is_key_pressed("R2"):
            GRIPPER_ANGLE.move_to(45, 50)
            power_expand_board.set_power(SPINNER_PORT, -100)
        elif gamepad.is_key_pressed("L2"):
            SPIN_TIG = True
            GRIPPER_ANGLE.move_to(45, 50)
            power_expand_board.set_power(SPINNER_PORT, -100)
        else:
            power_expand_board.set_power(SPINNER_PORT, 0)

        if gamepad.is_key_pressed("Up"):
            power_expand_board.set_power("DC4", 100)
        elif gamepad.is_key_pressed("Down") or gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC4", -100)
        else:
            power_expand_board.set_power("DC4", DC_LOCK_V)
        
        if gamepad.is_key_pressed("N2"):
            GRIPPER_ANGLE.move_to(90, 50)
        elif gamepad.is_key_pressed("N3"):
            GRIPPER_ANGLE.move_to(0, 50)
        elif gamepad.is_key_pressed("L1"):
            GRIPPER_ANGLE.move_to(45, 50)
        
# Button map for keymap 3, controls bottom recovery gripper
def S3_Keymap ():
    if gamepad.is_key_pressed("N1"):
        #Release
        BUTTOM_GRIPPER.move_to(6, 50)
    elif gamepad.is_key_pressed("N4"):
        #Grab Block
        BUTTOM_GRIPPER.move_to(71, 50)
    elif gamepad.is_key_pressed("N2"):
        #Grab pin top
        BUTTOM_GRIPPER.move_to(88, 50)
    elif gamepad.is_key_pressed("N3"):
        # Grab Pin Buttom
        BUTTOM_GRIPPER.move_to(81, 50)
    elif gamepad.is_key_pressed("L1"):
        # Grab Block 2
        BUTTOM_GRIPPER.move_to(72, 50)
    elif gamepad.is_key_pressed("R1"):
        # Grab Standing Pin Buttom
        BUTTOM_GRIPPER.move_to(81, 50)

    if gamepad.is_key_pressed("Down"):
        # BUTTOM_GRIPPER.move(-1, 100)
        BUTTOM_GRIPPER.move(-5, 100)
    elif gamepad.is_key_pressed("Up"):
        # BUTTOM_GRIPPER.move(1, 100)
        BUTTOM_GRIPPER.move(5, 100) 

# function to control buttom gripper maxium power draw to prvent over current cutoff
def Motor_Safety_CTL ():
    if BUTTOM_GRIPPER.get_value("current") > 500:
        BUTTOM_GRIPPER.set_power(0)

# Startup
power_expand_board.set_power("DC4", 100)
debug.show('S0', wait = False)
GRIPPER_ANGLE.move_to(45, 50)
BUTTOM_GRIPPER.move_to(2, 50)
BRUSHLESS_SERVO.move_to(0, 50)
Motor_Control(0, 0, 0, 0)

# FRONT_TOP_CAM.set_mode("color")

debug.show('OK!', wait = False)
power_expand_board.set_power("DC4", DC_LOCK_V)
# GRIPPER_LOCK.set_angle(0)

# main loop
while True:
    if not power_manage_module.is_auto_mode():
        debug.show(round(BRUSHLESS_SERVO.get_value("voltage"), 1))
    Motor_Safety_CTL()
    if button_1.is_pressed():
        debug.show('WAIT', wait=False)
        GRIPPER_ANGLE.move_to(45, 50)
        BUTTOM_GRIPPER.move_to(2, 50)
        BRUSHLESS_SERVO.move_to(0, 50)
        Motor_Control(0, 0, 0, 0)
        debug.show('DONE', wait=False)

    if power_manage_module.is_auto_mode():
        if not ENABLE_AUTO:
            debug.show('A D', wait=False)
        elif FRONT_L_RANGING.get_distance() == 0:
            debug.show('ASE', wait=False)
            Auto_Maintain_Grip()
        else:
            debug.show('A P', wait=False)
            FR_ENCODE_M1.set_power(0)
            BR_ENCODE_M2.set_power(0)
            FL_ENCODE_M3.set_power(0)
            BL_ENCODE_M4.set_power(0)
            # FRONT_TOP_CAM.set_mode("color")
            debug.show('A W', wait=False)

            if LEFT_RANGING.get_distance() < RIGHT_RANGING.get_distance():
                AUTO_SIDE = 'L'
            else:
                AUTO_SIDE = 'R'
            # avoid ball 2 blocks
            Auto_stage_new_2()

            # avoid ball 3 blocks (only deploy on left right)
            # Auto_stage2()

            # ULTIMATE TOOL
            # Auto_stage99()
    else:
        if gamepad.is_key_pressed("L2") and gamepad.is_key_pressed("R2"):
            debug.show('K1', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            power_expand_board.set_power(SPINNER_PORT, 0)
            CTLMODE = 1
        elif gamepad.is_key_pressed("L1") and gamepad.is_key_pressed("R1"):
            debug.show('K2', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            CTLMODE = 2
        elif gamepad.is_key_pressed("+") and gamepad.is_key_pressed("≡"):
            debug.show('K3', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            power_expand_board.set_power(SPINNER_PORT, 0)
            CTLMODE = 3

        if CTLMODE == 1:
            BUTTOM_GRIPPER.move_to(6, 50)
            Auto_Maintain_Grip(t_distance=32)
            Movement()
            S1_Keymap()
        elif CTLMODE == 2:
            BUTTOM_GRIPPER.move_to(6, 50)
            Movement()
            S2_Keymap()
            # Auto_Maintain_Grip_Range(14, 12)
            # Auto_Maintain_Grip()
        elif CTLMODE == 3:
            Auto_Maintain_Grip(t_distance=3)
            Movement(-1)
            S3_Keymap()