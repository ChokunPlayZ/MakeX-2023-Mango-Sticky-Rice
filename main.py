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
CTLMODE = 1


# 2,4,5,6
# stuff
FR_ENCODE = encoder_motor_class("M2", "INDEX1")
BR_ENCODE = encoder_motor_class("M5", "INDEX1")
FL_ENCODE = encoder_motor_class("M4", "INDEX1")
BL_ENCODE = encoder_motor_class("M6", "INDEX1")

# Cameras
# FRONT_TOP_CAM = smart_camera_class("PORT4", "INDEX1")

def Motor_Control(M1, M2, M3, M4):
    FR_ENCODE.set_power(M1)
    BR_ENCODE.set_power(M2)
    FL_ENCODE.set_power(M3)
    BL_ENCODE.set_power(M4)

def Motor_RPM(M1, M2, M3, M4):
    FR_ENCODE.set_speed(M1)
    BR_ENCODE.set_speed(M2)
    FL_ENCODE.set_speed(M3)
    BL_ENCODE.set_speed(M4)

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
        Motor_RPM(LYn, LYp, LYn, LYp)
    elif RXp > 5 or RXp < -5:
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

power_expand_board.set_power("DC4", 100)
Motor_Control(0, 0, 0, 0)


while True:
    if CTLMODE == 1:
        Movement()