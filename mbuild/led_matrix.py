class led_matrix_class() :
    def __init__(self, PORT, INDEX):
        """
        define the led matrix
        PORT, the port the senor is connected to on the novapi
        INDEX, the sensor number in the chain INDEX<1-10>
        """

    def show_image(self, pattern, x, y, time_s = 1):
        """
        show image at x or y, and if time is defined, how many secionds
        """
        return
    
    def show(self, text, wait=False, pos_x=0, pos_y=0):
        "show text, and wait or not"
        return
    
    def clear(self):
        """clear display"""
        return
    def set_pixel(self, x, y, state):
        """turn pixel at x,y on or off"""
        return
    
    def toggle_pixel(self, x, y):
        """toggle pixel at xy"""
        return