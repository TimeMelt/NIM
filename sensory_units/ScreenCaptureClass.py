import logging
from Config import settings
from PIL import ImageGrab, Image
import numpy as np

class ScreenCapture():
    def __init__(self):
        super().__init__()
        self.n_wires = settings["n_wires"]
    
    def log_and_print(self, float_array):
        logging.basicConfig(filename=f"{settings['log_dir']}/screen-capture.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
        logging.info(f"screen capture array: {float_array} \n")

    def return_value(self):
        screenshot = ImageGrab.grab()
        rgb_screenshot = screenshot.convert('RGB')
        resized_screenshot = rgb_screenshot.resize((1, 1), Image.Resampling.LANCZOS)
        arr_uint8 = np.array(resized_screenshot).flatten()
        arr_float = arr_uint8.astype(np.float32)
        arr_normalized = arr_float / 255.0
        
        self.log_and_print(arr_normalized)
        
        return arr_normalized
            