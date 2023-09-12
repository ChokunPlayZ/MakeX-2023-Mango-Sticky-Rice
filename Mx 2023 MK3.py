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

# stuff
BR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
FR_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
BL_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
FL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")
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
smart_camera_1 = smart_camera_class("PORT4", "INDEX1")
led_matrix_1 = led_matrix_class("PORT4", "INDEX1")
button_1 = button_class("PORT4", "INDEX1")

def Motor_Control(M1, M2, M3, M4):
    BR_ENCODE_M1.set_power(M1)
    FR_ENCODE_M2.set_power(M2)
    BL_ENCODE_M3.set_power(M3)
    FL_ENCODE_M4.set_power(M4)

def Motor_RPM(M1, M2, M3, M4):
    BR_ENCODE_M1.set_speed(M1)
    FR_ENCODE_M2.set_speed(M2)
    BL_ENCODE_M3.set_speed(M3)
    FL_ENCODE_M4.set_speed(M4)

def Auto_Grip ():
    GRIPPER_ANGLE.move_to(45, 50)
    power_expand_board.set_power("DC5", 100)
    Motor_RPM(100, 100, -100, -100)
    while FRONT_L_RANGING.get_distance() > 8:
        led_matrix_1.show(FRONT_L_RANGING.get_distance(), wait=False)
        time.sleep(0.001)
    power_expand_board.set_power("DC5", 0)
    Motor_Control(-2, -2, 2, 2)

    while FRONT_L_RANGING.get_distance() < 20:
        time.sleep(0.001)
        Motor_RPM(-100, -100, 100, 100)
    Motor_Control(2, 2, -2, -2)

    target_angle = novapi.get_yaw() + 85
    while novapi.get_yaw() < target_angle :
        time.sleep(0.001)
        Motor_RPM(-100, -100, -100, -100)
    Motor_Control(2, 2, 2, 2)

    power_expand_board.set_power("DC5", -100)
    time.sleep(1)
    power_expand_board.set_power("DC5", 0)

    target_angle = novapi.get_yaw() - 80
    while novapi.get_yaw() > target_angle :
        time.sleep(0.001)
        Motor_RPM(100, 100, 100, 100)
    Motor_Control(-2, -2, -2, -2)



def Auto_stage():
    global ENABLE_AUTO, V_AUTO_STAGE
    if ENABLE_AUTO == 0:
        led_matrix_1.show('A D', wait=False)
        return
    if ENABLE_AUTO == 1:
        led_matrix_1.show('A P', wait=False)
        BR_ENCODE_M1.set_power(0)
        FR_ENCODE_M2.set_power(0)
        BL_ENCODE_M3.set_power(0)
        FL_ENCODE_M4.set_power(0)
        smart_camera_1.open_light()
        smart_camera_1.set_mode("color")
        led_matrix_1.show('A W', wait=False)

        if LEFT_RANGING.get_distance() > RIGHT_RANGING.get_distance():
            AUTO_SIDE = 'R'
        else:
            AUTO_SIDE = 'L'

        while power_manage_module.is_auto_mode():
            led_matrix_1.show('A' + str(str(AUTO_SIDE) + str(V_AUTO_STAGE)), wait=False)

            if GRIPPER_RANGING.get_distance() > 20:
                power_expand_board.set_power("DC4", -100)
            elif GRIPPER_RANGING.get_distance() < 15:
                power_expand_board.set_power("DC4", 10)
            else:
                power_expand_board.set_power("DC4", DC_LOCK_V)

            if V_AUTO_STAGE == 0:
                if AUTO_SIDE == "L":
                    target_angle = novapi.get_yaw() - 30
                    while novapi.get_yaw() > target_angle :
                        time.sleep(0.001)
                        Motor_RPM(100, 100, 100, 100)
                    Motor_Control(-2, -2, -2, -2)
                    V_AUTO_STAGE = V_AUTO_STAGE + 1
                elif AUTO_SIDE == "R":
                    target_angle = novapi.get_yaw() + 30
                    while novapi.get_yaw() < target_angle :
                        time.sleep(0.001)
                        Motor_RPM(-100, -100, -100, -100)
                    Motor_Control(2, 2, 2, 2)
                    V_AUTO_STAGE = V_AUTO_STAGE + 1
                else:
                    led_matrix_1.show('AE', wait=False)
                    time.sleep(500)

            if V_AUTO_STAGE == 1:
                if FRONT_L_RANGING.get_distance() > 20:
                    Motor_RPM(100, 100, -100, -100)
                else:
                    Motor_Control(-2, -2, 2, 2)
                    V_AUTO_STAGE = V_AUTO_STAGE + 1

            if V_AUTO_STAGE == 0:
                if AUTO_SIDE == "L":
                    target_angle = novapi.get_yaw() + 30
                    while novapi.get_yaw() < target_angle :
                        time.sleep(0.001)
                        Motor_RPM(-100, -100, -100, -100)
                    Motor_Control(-2, -2, -2, -2)
                    V_AUTO_STAGE = V_AUTO_STAGE + 1
                elif AUTO_SIDE == "R":
                    target_angle = novapi.get_yaw() - 30
                    while novapi.get_yaw() > target_angle :
                        time.sleep(0.001)
                        Motor_RPM(100, 100, 100, 100)
                    Motor_Control(2, 2, 2, 2)
                    V_AUTO_STAGE = V_AUTO_STAGE + 1
                else:
                    led_matrix_1.show('AE', wait=False)
                    time.sleep(500)

            # if V_AUTO_STAGE == 1:
            #     while V_AUTO_STAGE == 1:
            #         # walk right until the smart camera detect block 1 at arround center
            #         if smart_camera_1.detect_sign_location(1, "middle"):
            #             Motor_Control(0, 0, 0, 0)
            #             V_AUTO_STAGE = V_AUTO_STAGE + 1
            #         else :
            #             Motor_Control(100,-100, -100, 100)


        # Stop all motors when the loop ends
        BR_ENCODE_M1.set_power(0)
        FR_ENCODE_M2.set_power(0)
        BL_ENCODE_M3.set_power(0)
        FL_ENCODE_M4.set_power(0)

        led_matrix_1.show('A E', wait=False)
        return

## END
## END
## END
def Movement ():
    LYp = gamepad.get_joystick("Ly") / Speed_Modifier
    LYn = LYp * -1
    LXp = gamepad.get_joystick("Lx") / Speed_Modifier
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") / Speed_Modifier
    RXn = RXp * -1
    TURN_SPEED = RXn / TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_Control(LYn, LYn, LYp, LYp)
    elif LXp > 5 or LXp < -5:
        Motor_Control(LXp, LXn, LXp, LXn)
    elif RXp > 5 or RXp < -5:
        Motor_Control(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_Control(0, 0, 0, 0)

def Reverse_movement ():
    LYp = gamepad.get_joystick("Ly") / Speed_Modifier
    LYn = LYp * -1
    LXp = gamepad.get_joystick("Lx") / Speed_Modifier
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") / Speed_Modifier
    RXn = RXp * -1
    TURN_SPEED = RXn / TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_Control(LYp, LYp, LYn, LYn)
    elif LXp > 5 or LXp < -5:
        Motor_Control(LXn, LXp, LXn, LXp)
    elif RXp > 5 or RXp < -5:
        Motor_Control(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_Control(0, 0, 0, 0)

def S1_Keymap ():
    if gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC1", 100)
        power_expand_board.set_power("DC2", 100)

    if gamepad.is_key_pressed("Right"):
        power_expand_board.set_power("DC2", -100)
    elif gamepad.is_key_pressed("Left"):
        power_expand_board.set_power("DC1", -100)
    elif gamepad.is_key_pressed("Up"):
        power_expand_board.set_power("DC1", 0)
        power_expand_board.set_power("DC2", 0)

    if gamepad.is_key_pressed("L1"):
        power_expand_board.set_power("DC1", 0)
        power_expand_board.set_power("DC2", 0)

    if gamepad.is_key_pressed("N2"):
        power_expand_board.set_power("DC3", -100)
    elif gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("DC3", 100)
    else:
        power_expand_board.set_power("DC3", 0)

    if gamepad.is_key_pressed("N4"):
        power_expand_board.set_power("BL1", 100)
        power_expand_board.set_power("BL2", 100)
    elif gamepad.is_key_pressed("R1"):
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")

    if gamepad.is_key_pressed("+"):
        BRUSHLESS_SERVO.move_to(-9, 100)
    elif gamepad.is_key_pressed("≡"):
            BRUSHLESS_SERVO.move_to(2, 100)

    if gamepad.is_key_pressed("R_Thumb"):
        power_expand_board.set_power("DC2", 100)
        power_expand_board.set_power("DC1", 0)
    elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power("DC1", 0)

def S2_Keymap ():
    if gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC5", 100)
        power_expand_board.set_power("DC4", 100)
    elif gamepad.is_key_pressed("N4"):
        power_expand_board.set_power("DC5", -100)
    elif gamepad.is_key_pressed("R1"):
        power_expand_board.set_power("DC5", 100)
    else:
        power_expand_board.set_power("DC5", 0)

        if gamepad.is_key_pressed("Up"):
            power_expand_board.set_power("DC4", -100)
        elif gamepad.is_key_pressed("Down"):
            power_expand_board.set_power("DC4", 100)
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
        BUTTOM_GRIPPER.move_to(0, 50)
    elif gamepad.is_key_pressed("N4"):
        #Grab Block
        BUTTOM_GRIPPER.move_to(-73, 50)
    elif gamepad.is_key_pressed("N2"):
        #Grab pin top
        BUTTOM_GRIPPER.move_to(-94, 50)
    elif gamepad.is_key_pressed("N3"):
        # Grab Pin Buttom
        BUTTOM_GRIPPER.move_to(-85, 50)
    elif gamepad.is_key_pressed("L1"):
        # Grab Block 2
        BUTTOM_GRIPPER.move_to(-75, 50)
    elif gamepad.is_key_pressed("R1"):
        # Grab Pin Buttom
        BUTTOM_GRIPPER.move_to(-86, 50)

    if gamepad.is_key_pressed("Down"):
        BUTTOM_GRIPPER.move(3, 100)
    elif gamepad.is_key_pressed("Up"):
            BUTTOM_GRIPPER.move(-3, 100)

def feeder_control ():
    if gamepad.is_key_pressed("N1"):
        if B1_ST == 1:
            power_expand_board.set_power("DC1", 100)
            power_expand_board.set_power("DC2", 100)
            B1_ST = 0
        else:
            power_expand_board.set_power("DC1", 0)
            power_expand_board.set_power("DC2", 0)
            B1_ST = 0
        time.sleep(0.2)
    if gamepad.is_key_pressed("L1"):
        if L1_ST == 1:
            power_expand_board.set_power("DC2", 100)
            L1_ST = 0
        else:
            power_expand_board.set_power("DC2", 0)
            L1_ST = 0
        time.sleep(0.2)

def Motor_Safety_CTL ():
    if BUTTOM_GRIPPER.get_value("current") > 500:
        BRUSHLESS_SERVO.set_power(0)

# Control System Config
Speed_Modifier = 1.6 # หหารความเร็วด้วย
TURN_SPEED_MODIFIER = 1.3
CTLMODE = 2
DC_LOCK_V = -5

# Automatic Stage Config
ENABLE_AUTO = 1
V_AUTO_STAGE = 0
AUTO_RPM = 150
NEG_AUTO_RPM = -150

AUTO_SIDE = None

power_expand_board.set_power("DC4", -100)
led_matrix_1.show('S0', wait = False)
GRIPPER_ANGLE.move_to(45, 50)
BUTTOM_GRIPPER.move_to(0, 50)
BRUSHLESS_SERVO.move_to(0, 50)
Motor_Control(0, 0, 0, 0)
# while not (GRIPPER_RANGING.get_distance() < 3.5 or GRIPPER_RANGING.get_distance() == 200):
#     time.sleep(0.001)
#     power_expand_board.set_power("DC4", -100)

# power_expand_board.set_power("DC4", DC_LOCK_V)
led_matrix_1.show('OK!', wait = False)
power_expand_board.set_power("DC4", DC_LOCK_V)

# Motor_Control(10,0,0,0)
# time.sleep(1)
# Motor_Control(0,10,0,0)
# time.sleep(1)
# Motor_Control(0,0,10,0)
# time.sleep(1)
# Motor_Control(0,0,0,10)
# time.sleep(1)

while True:
    # led_matrix_1.show(round(smart_camera_1.get_sign_x(1), 1))
    # led_matrix_1.show(round(novapi.timer(), 1))
    # led_matrix_1.show(smart_camera_1.detect_sign_location(1, "middle"))
    # if smart_camera_1.detect_sign_location(1, "middle"): 
    #     led_matrix_1.show('t', wait = False)
    # else:
    #     led_matrix_1.show('f', wait = False)
    # led_matrix_1.show(BUTTOM_GRIPPER.get_value("angle"), wait=False)
    # led_matrix_1.show(FRONT_L_RANGING.get_distance(), wait=False)
    # led_matrix_1.show(novapi.get_yaw(), wait=False)
    led_matrix_1.show(GRIPPER_RANGING.get_distance(), wait=False)
    Motor_Safety_CTL()
    if button_1.is_pressed():
        Auto_Grip()
        # V_AUTO_STAGE = 0
        # ENABLE_AUTO = 1
        # smart_camera_1.open_light()
        # smart_camera_1.reset()
        # smart_camera_1.close_light()

    if power_manage_module.is_auto_mode():
        Auto_stage()
    else:
        if gamepad.is_key_pressed("L2") and gamepad.is_key_pressed("R2"):
            led_matrix_1.show('K1', wait = False)
            CTLMODE = 1
        elif gamepad.is_key_pressed("L1") and gamepad.is_key_pressed("R1"):
            led_matrix_1.show('K2', wait = False)
            CTLMODE = 2
        elif gamepad.is_key_pressed("+") and gamepad.is_key_pressed("≡"):
            led_matrix_1.show('K3', wait = False)
            CTLMODE = 3

        if CTLMODE == 1:
            BUTTOM_GRIPPER.move_to(0, 50)
            Movement()
            S1_Keymap()
        elif CTLMODE == 2:
            BUTTOM_GRIPPER.move_to(0, 50)
            Reverse_movement()
            S2_Keymap()
        elif CTLMODE == 3:
            Reverse_movement()
            S3_Keymap()