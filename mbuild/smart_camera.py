#note Only Block color and Line follower is implemented, no other stuff just yet
class smart_camera_class() :
    def __init__(self, PORT, INDEX):
        """
        define the smart camera
        PORT, the port the senor is connected to on the novapi
        INDEX, the sensor number in the chain INDEX<1-10>
        """
    
    def set_mode(self, mode:str):
        """set smart camera mode to
        avaible mode: "color", "line"
        """
        return
    
    def learn(self, block:int, until:str):
        """learn a block until a button is pressed
        Block: 1,2,3,4,5,6,7
        ```
        .learn(<block>, "until_button")
        ```
        """
        return
    
    def open_light(self):
        """open flood light"""
        return

    def close_light(self):
        """close flood light"""
        return
    
    def reset(self):
        """reset white balance"""
        return
    
    def detect_sign(self, block:int):
        """check if smart camera detect a block"""
        return

    def detect_sign_location(self, block:int, location:str):
        """
        check if smart camera detected block at location
        avaible location
        middle, up, down, left, right"""
        return
    
    def get_sign_x(self, block:int):
        """
        get x location of a block
        """
        return
    
    def get_sign_y(self, block:int):
        """
        get y location of a block
        """
        return
    
    def get_sign_wide(self, block:int):
        """
        get width of a block
        """
        return
    
    def get_sign_height(self, block:int):
        """
        get height of a block
        """
        return
    
    def set_line(self, color:str):
        """
        set line color
        color: black/white
        """
        return