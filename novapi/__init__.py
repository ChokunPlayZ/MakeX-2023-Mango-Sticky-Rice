## Timer Module
def timer():
    "Get the system timer time in seconds."
    return 1

def reset_timer():
    "Reset the system timer time."
    return 0

#Built in Gyro
def get_pitch():
    "Obtain the pitch angle (X axis) of the attitude angle, unit: °, the returned data range is-180 ~ 180"
    return 0

def get_roll():
    "Get the roll angle (Y axis) of the attitude angle, unit: °, the returned data range is-180 ~ 180"
    return 0

def get_yaw():
    "Get the yaw angle (Z axis) of the attitude angle, unit: °, the returned data range is , because the onboard gyroscope module is a six-axis sensor, there is no electronic compass. So actually the yaw angle just uses the integral of the Z-axis angular velocity. It has accumulated errors. If you want to get the real yaw angle, this API is not suitable for use.-32768 ~ 32767"
    return 0

def is_shaked():
    "Detect whether the onboard gyroscope module is shaken, the return value is a Boolean value, where Truemeans the gyroscope module is shaken, Falsemeans the gyroscope module is not shaken."
    return False

def get_acceleration(axis:str):
    """Get the acceleration values ​​of the three axes, the unit is g, parameters:

    axis is a string type, starting with x, y, zrepresenting the coordinate axis defined by the onboard gyroscope module.
    def get_gyroscope(axis:str)
    Get the angular velocity values ​​of the three axes, the unit is °/秒, the returned data range is , parameters -500 ~ 500

    axis is a string type, starting with x, y, zrepresenting the coordinate axis defined by the onboard gyroscope module.
    def set_shake_threshold( threshold )
    Set the vibration threshold, parameters

    threshold vibration threshold, the range is ``0~100``, the system default vibration threshold is 50, 0 means to disable vibration detection.
    """
    return

def get_gyroscope(axis:str):
    """
    get the angular speed of the specified axis, in deg/s
    """

def reset_rotation(axis:str):
    """
    Reset the angle rotated around the x, y, z axis, parameters:

    axis string type, with x, y, z, allrepresenting the coordinate axes defined by the onboard gyroscope module, `all` represents all axes.
    """
    return None