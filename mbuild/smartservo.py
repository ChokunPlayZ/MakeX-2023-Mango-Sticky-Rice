class smartservo_class() :
    def __init__(self, port:str, index:str):
        """
        initilize an smart servo  
        Port: M1,M2,M3,M4,M5,M6  
        Index, INDEX<no> (1-6)  
        """
        pass

    def set_power(self, power:int):
        """
        Set smart servo power by percent
        """
        return power
    
    def move(self, angle:int, speeed:int):
        """
        rotate smart servo by angle at speed
        """
        return angle
    
    def move_to(self, angle:int, speeed:int):
        """
        rotate smart servo to angle at speed
        """
        return angle
    
    def get_value(self, value:str):
        """
        get the requested value from the smart servo
        Value avaible: "current", "voltage", "speed", "angle", "temperature"
        """
        return value