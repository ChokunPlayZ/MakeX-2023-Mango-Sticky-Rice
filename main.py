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

# Control System Config
Speed_Modifier = 2.5
Speed_Modifier2 = 1.2
TURN_SPEED_MODIFIER = 1.5
CTLMODE = 2
DC_LOCK_V = 6

FEEDER_POWER = 50

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
led_matrix_1 = led_matrix_class("PORT4", "INDEX1")
button_1 = button_class("PORT4", "INDEX1")

# Cameras
FRONT_TOP_CAM = smart_camera_class("PORT4", "INDEX1")

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

def Move_Dia_LR(rpm):
    """Move Diagonal Left and Right (+rpm for Right, -rpm for Left)"""
    Motor_RPM(rpm * -1, 0, 0, rpm)

def Move_Dia_FB(rpm):
    """Move Diagonal Forward and Backward (+rpm for Forward, -rpm for Backward)"""
    Motor_RPM(rpm, 0, 0, rpm * -1)

def Move_Turn(rpm):
    """Turn Left or Right (+rpm for Left, -rpm for Right)"""
    Motor_RPM(rpm, rpm, rpm, rpm)

def Auto_Maintain_Grip(t_distance=14):
    distance = GRIPPER_RANGING.get_distance()

    power = abs(distance - t_distance) * 4  # Calculate power based on distance from target

    if distance > t_distance:
        power_expand_board.set_power("DC4", power)
    elif distance < t_distance:
        power_expand_board.set_power("DC4", -power)
    else:
        power_expand_board.set_power("DC4", DC_LOCK_V)

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
        led_matrix_1.show('A' + str(str(AUTO_SIDE) + str(V_AUTO_STAGE)), wait=False)

        Auto_Maintain_Grip()

        if V_AUTO_STAGE == 0:
            while FRONT_L_RANGING.get_distance() > 20:
                time.sleep(0.001)
                Auto_Maintain_Grip()
                power_expand_board.set_power("DC5", -100)
                Move_FB(AUTO_RPM)
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            
        elif V_AUTO_STAGE == 1:
            power_expand_board.set_power("DC5", -100)
            if FRONT_L_RANGING.get_distance() > 7:
                Move_FB(100)
            elif No_Drift():
                if AUTO_SIDE == "R": 
                    if LEFT_RANGING.get_distance() < 20:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(-85, 80, -85, 80)
                else:
                    if RIGHT_RANGING.get_distance() < 20:
                        Move_FB(0)
                        V_AUTO_STAGE = V_AUTO_STAGE + 1
                        continue
                    else:
                        Motor_Control(85, -80, 85, -80)
        elif V_AUTO_STAGE == 2:
            Move_FB(0)
            power_expand_board.set_power("DC5", 0)
            V_AUTO_STAGE = V_AUTO_STAGE + 1
            continue

## END
## END
## END
def Movement ():
    LYp = gamepad.get_joystick("Ly") * Speed_Modifier
    LYn = LYp * -1
    LXp = gamepad.get_joystick("Lx") * Speed_Modifier2
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") * Speed_Modifier
    RXn = RXp * -1
    TURN_SPEED = RXn * TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_RPM(LYn, LYn, LYp, LYp)
    elif LXp > 5 or LXp < -5:
        Motor_RPM(LXp, LXn, LXp, LXn)
    elif RXp > 5 or RXp < -5:
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

def Reverse_movement ():
    LYp = gamepad.get_joystick("Ly") * Speed_Modifier
    LYn = LYp * -1
    LXp = gamepad.get_joystick("Lx") * Speed_Modifier2
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") * Speed_Modifier
    RXn = RXp * -1
    TURN_SPEED = RXn * TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_RPM(LYp, LYp, LYn, LYn)
    elif LXp > 5 or LXp < -5:
        Motor_RPM(LXn, LXp, LXn, LXp)
    elif RXp > 5 or RXp < -5:
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

def S1_Keymap ():
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
        power_expand_board.set_power("DC8", 100)
    elif gamepad.is_key_pressed("R1"):
        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")
        power_expand_board.stop("DC8")

    # Brushless Angle
    if gamepad.is_key_pressed("+"):
        BRUSHLESS_SERVO.move_to(-23, 100)
        # BRUSHLESS_SERVO.move(1, 50)
    elif gamepad.is_key_pressed("≡"):
        BRUSHLESS_SERVO.move_to(2, 100)
        # BRUSHLESS_SERVO.move(-1, 50)

    if gamepad.is_key_pressed("R_Thumb"):
        power_expand_board.set_power("DC2", 100)
        power_expand_board.set_power("DC1", 0)
    elif gamepad.is_key_pressed("L2"):
        power_expand_board.set_power("DC1", 0)

def S2_Keymap ():
    global SPIN_TIG
    if SPIN_TIG:
        Auto_Maintain_Grip()
        if gamepad.is_key_pressed("≡"):
            SPIN_TIG = False
            power_expand_board.set_power("DC5", 0)
    else:
        if gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC5", 100)
        elif gamepad.is_key_pressed("N4"):
            power_expand_board.set_power("DC5", -100)
        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC5", 100)
        elif gamepad.is_key_pressed("R2"):
            GRIPPER_ANGLE.move_to(45, 50)
            power_expand_board.set_power("DC5", -100)
        elif gamepad.is_key_pressed("L2"):
            SPIN_TIG = True
            GRIPPER_ANGLE.move_to(45, 50)
            power_expand_board.set_power("DC5", -100)
        else:
            power_expand_board.set_power("DC5", 0)

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
        
def S3_Keymap ():
    if gamepad.is_key_pressed("N1"):
        #Release
        BUTTOM_GRIPPER.move_to(2, 50)
    elif gamepad.is_key_pressed("N4"):
        #Grab Block
        BUTTOM_GRIPPER.move_to(71, 50)
    elif gamepad.is_key_pressed("N2"):
        #Grab pin top
        BUTTOM_GRIPPER.move_to(85, 50)
    elif gamepad.is_key_pressed("N3"):
        # Grab Pin Buttom
        BUTTOM_GRIPPER.move_to(79, 50)
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

def Motor_Safety_CTL ():
    if BUTTOM_GRIPPER.get_value("current") > 500:
        BRUSHLESS_SERVO.set_power(0)

power_expand_board.set_power("DC4", 100)
led_matrix_1.show('S0', wait = False)
GRIPPER_ANGLE.move_to(45, 50)
BUTTOM_GRIPPER.move_to(2, 50)
BRUSHLESS_SERVO.move_to(0, 50)
Motor_Control(0, 0, 0, 0)

FRONT_TOP_CAM.set_mode("color")

led_matrix_1.show('OK!', wait = False)
power_expand_board.set_power("DC4", DC_LOCK_V)
# GRIPPER_LOCK.set_angle(0)

while True:
    if not power_manage_module.is_auto_mode():
        led_matrix_1.show(round(BRUSHLESS_SERVO.get_value("voltage"), 1))
        # led_matrix_1.show(BUTTOM_GRIPPER.get_value("angle"), wait=False)
        # led_matrix_1.show(button_1.is_pressed(), wait=False)
        # led_matrix_1.show(RIGHT_RANGING.get_distance(), wait=False)
    Motor_Safety_CTL()
    if button_1.is_pressed():
        # GRIPPER_LOCK.set_angle(60)
        # auto_align_and_grip()
        # FRONT_TOP_CAM.set_mode("color")
        # FRONT_MID_CAM.set_mode("color")

        FRONT_TOP_CAM.open_light()
        time.sleep(1)
        FR_ENCODE_M1.set_power(100)
        time.sleep(1)
        FR_ENCODE_M1.set_power(0)
        time.sleep(1)
        BR_ENCODE_M2.set_power(100)
        time.sleep(1)
        BR_ENCODE_M2.set_power(0)
        time.sleep(1)
        FL_ENCODE_M3.set_power(100)
        time.sleep(1)
        FL_ENCODE_M3.set_power(0)
        time.sleep(1)
        BL_ENCODE_M4.set_power(100)
        time.sleep(1)
        BL_ENCODE_M4.set_power(0)
        FRONT_TOP_CAM.close_light()

        # GRIPPER_LOCK.set_angle(0)

    if power_manage_module.is_auto_mode():
        if not ENABLE_AUTO:
            led_matrix_1.show('A D', wait=False)
        elif FRONT_L_RANGING.get_distance() == 0:
            led_matrix_1.show('ASE', wait=False)
            Auto_Maintain_Grip()
        else:
            led_matrix_1.show('A P', wait=False)
            FR_ENCODE_M1.set_power(0)
            BR_ENCODE_M2.set_power(0)
            FL_ENCODE_M3.set_power(0)
            BL_ENCODE_M4.set_power(0)
            FRONT_TOP_CAM.set_mode("color")
            led_matrix_1.show('A W', wait=False)

            if LEFT_RANGING.get_distance() < RIGHT_RANGING.get_distance():
                AUTO_SIDE = 'L'
            else:
                AUTO_SIDE = 'R'
            # avoid ball 2 blocks
            Auto_stage_new_1()

            # avoid ball 3 blocks (only deploy on left right)
            # Auto_stage2()

            # ULTIMATE TOOL
            # Auto_stage99()
    else:
        if gamepad.is_key_pressed("L2") and gamepad.is_key_pressed("R2"):
            led_matrix_1.show('K1', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            power_expand_board.set_power("DC5", 0)
            CTLMODE = 1
        elif gamepad.is_key_pressed("L1") and gamepad.is_key_pressed("R1"):
            led_matrix_1.show('K2', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            CTLMODE = 2
        elif gamepad.is_key_pressed("+") and gamepad.is_key_pressed("≡"):
            led_matrix_1.show('K3', wait = False)
            power_expand_board.set_power("DC4", DC_LOCK_V)
            power_expand_board.set_power("DC5", 0)
            CTLMODE = 3

        if CTLMODE == 1:
            BUTTOM_GRIPPER.move_to(2, 50)
            Auto_Maintain_Grip(t_distance=35)
            Movement()
            S1_Keymap()
        elif CTLMODE == 2:
            BUTTOM_GRIPPER.move_to(2, 50)
            Reverse_movement()
            S2_Keymap()
        elif CTLMODE == 3:
            Auto_Maintain_Grip(t_distance=5)
            Reverse_movement()
            S3_Keymap()