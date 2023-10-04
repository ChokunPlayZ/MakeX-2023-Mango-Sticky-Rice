class servo_driver_class:
    def __init__(self, PORT, INDEX):
        """
        define the servo driver
        PORT, the port the senor is connected to on the novapi
        INDEX, the sensor number in the chain INDEX<1-10>
        """
        pass

    def set_angle(self, angle:int):
        """set servo to an angle"""
        pass

    def change_angle(self, angle:int):
        """set servo to and angle"""
        pass

    def get_angle(self):
        """get the current servo angle"""
        pass