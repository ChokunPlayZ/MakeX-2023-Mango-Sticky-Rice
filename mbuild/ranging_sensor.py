class ranging_sensor_class() :
    def __init__(self, PORT, INDEX):
        """
        define the raning sensor
        PORT, the port the senor is connected to on the novapi
        INDEX, the sensor number in the chain INDEX<1-10>
        """
    
    def get_distance(self):
        """
        Get the ranging sensor distance, range 2~200 cm
        """