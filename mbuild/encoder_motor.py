class encoder_motor_class() :
    def __init__(self, port:str, index:str):
        """
        initilize an encoder motor
        Port: M1,M2,M3,M4,M5,M6
        Index, INDEX<no> (1-6)
        """
        pass

    def set_power(self, power:int):
        """
        Set encoder motor power by percent
        """
        return power
    
    def set_speed(self, speed:int):
        """
        Set encoder motor by RPM (max 180)
        """
        return speed
    
    def move(self, angle:int, speeed:int):
        """
        rotate encoder motor by angle at speed
        """
        return angle
    
    def move_to(self, angle:int, speeed:int):
        """
        rotate encoder motor to angle at speed
        """
        return angle
    
    def get_value(self, value:str):
        """
        get the requested value from the encoder motor
        Value avaible: "speed", "angle"
        """
        return value