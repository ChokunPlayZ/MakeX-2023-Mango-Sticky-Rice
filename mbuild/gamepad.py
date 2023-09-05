def get_joystick(joystick:str):
    """Get the joystick value, return value range , left positive and right negative, up positive and bottom negative, parameters:100 ~ -100
    ```
    {
        "Lx": "left x-axis",
        "Ly": "left y-axis",
        "Rx": "right x-axis",
        "Ry": "right y-axis"
    }
    ```
    """

def is_key_pressed(button:str):
    """
    Get the status of the button on the makeblock joystick
    ```
    {
        "R1": "Right R1",
        "R2": "Right R2",
        "L1": "Left L1",
        "L2": "Left L2",
        "N1": "Number 1",
        "N2": "Number 2",
        "N3": "Number 3",
        "N4": "Number 4",
        "Up": "Arrow key up",
        "Down": "Arrow key down",
        "Left": "Arrow key left",
        "Right": "Arrow key right",
        "+": "Plus Key",
        “≡“: "Menu key",
        "L_Thumb": "left joystick pressed",
        "R_Thumb": "right joystick pressed"
    }
    ```
    """
