# code make you sleepy
# https://makex.ckl.moe/lol
import novapi
from mbuild import power_manage_module
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild.led_matrix import led_matrix_class
import mbuild
import time

# stuff
BR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
FR_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
BL_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
FL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")

# Servos
BRUSHLESS_SERVO = smartservo_class("M5", "INDEX1")

# Debugging Hardware
led_matrix_1 = led_matrix_class("PORT4", "INDEX1")

def Motor_Control(M1, M2, M3, M4):
    BR_ENCODE_M1.set_power(M1)
    FR_ENCODE_M2.set_power(M2)
    BL_ENCODE_M3.set_power(M3)
    FL_ENCODE_M4.set_power(M4)  

# Control System Config
Speed_Modifier = 1.6
TURN_SPEED_MODIFIER = 1.3
CTLMODE = 2

led_matrix_1.show('S0', wait = False)
BRUSHLESS_SERVO.move_to(0, 50)
Motor_Control(0, 0, 0, 0)

led_matrix_1.show('OK!', wait = False)
# GRIPPER_LOCK.set_angle(0)

while True:
    if not power_manage_module.is_auto_mode():
        led_matrix_1.show(round(BRUSHLESS_SERVO.get_value("voltage"), 1))

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
        power_expand_board.set_power("DC3", 100)
    elif gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("DC3", -100)
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
        BRUSHLESS_SERVO.move_to(-13, 100)
        # BRUSHLESS_SERVO.move(1, 50)
    elif gamepad.is_key_pressed("≡"):
        BRUSHLESS_SERVO.move_to(-3, 100)
        # BRUSHLESS_SERVO.move(-1, 50)

    if gamepad.is_key_pressed("R_Thumb"):
        power_expand_board.set_power("DC2", 100)
        power_expand_board.set_power("DC1", 0)
    elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power("DC1", 0)