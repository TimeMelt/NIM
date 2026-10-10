"""
    Screen Capture Input
    ====================

    this circuit grabs input by taking periodic screenshots of the display contents
        - executes everytime an inceptron epoch initiates
        - in order to use this the number of qubits/wires in each inceptron needs to be multiples of 3
            - screenshots use RGB format which requires at least 3 qubits and can only increase in multiples of 3 such as (3,6,9...etc)
        - generated logs show up at /logs/screen-capture.log
"""

import logging
from Config import settings
from PIL import ImageGrab, Image
import numpy as np

class ScreenCapture():
    def __init__(self):
        super().__init__()
        self.n_wires = settings["n_wires"]
        self.resize_rgb = int(self.n_wires / 3)  # calculate size value needed based on number of qubits/wires
    
    def log_and_print(self, float_array):
        logging.basicConfig(filename=f"{settings['log_dir']}/screen-capture.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
        logging.info(f"screen capture array: {float_array} \n")

    def return_value(self):
        screenshot = ImageGrab.grab()
        rgb_screenshot = screenshot.convert('RGB')
        resized_screenshot = rgb_screenshot.resize((1, self.resize_rgb), Image.Resampling.LANCZOS)
        arr_uint8 = np.array(resized_screenshot).flatten()
        arr_float = arr_uint8.astype(np.float32)
        arr_normalized = arr_float / 255.0
        
        self.log_and_print(arr_normalized)
        
        return arr_normalized
            