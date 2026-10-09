"""
    Audio Input
    ===========

    This circuit grabs audio input data using the microphone (default device set in OS)
        - executes everytime an inceptron epoch initiates
        - sample rate, number of channels, and block size are configurable
            - sample rate: frequency which audio is recorded
            - number of channels: 1 for mono, 2 for stereo
            - block size: larger block size outputs means more data values, data sampling is automatic based on number of
            qubits/wires per inceptron (grabs first N number of values, where N = number of qubits/wires), best to leave at default unless specific roadblock arise

"""

import queue
import sys, logging
import sounddevice as sd
import threading
from Config import settings
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): pass

class AudioStream(threading.Thread):
    def __init__(self):
        super().__init__()
        self.audio_queue = queue.Queue()   # Thread-safe queue to hold audio chunks
        self.queue_manager = QueueManager(address=(settings["queue_address"], settings["queue_port"]), authkey=settings["queue_authkey"])

    def audio_callback(self, indata, frames, time, status):
        """This is called for each audio buffer by sounddevice."""
        if status:
            print(status, file=sys.stderr)
        # indata is already a numpy array of floats when dtype='float32'
        # We put a copy into the queue to process safely in the main thread
        self.audio_queue.put(indata.copy())

    def push2Queues(self, weights, i):
        setattr(self.queue_manager, f"get_queue_{i}", weights)

    def log_and_print(self, float_array):
        logging.basicConfig(filename=f"{settings['log_dir']}/audio.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
        logging.info(f"audio array: {float_array} \n")

    def return_value(self):
        try:
            # Start the continuous microphone stream
            with sd.InputStream(samplerate=settings["audio_sample_rate"],
                                channels=settings["audio_channel_number"],
                                blocksize=settings["audio_block_size"],
                                dtype='float32',  # Forces 32-bit floating point numbers (-1.0 to 1.0)
                                callback=self.audio_callback):
                        
                # Get the next chunk of audio from the queue (blocks until available)
                audio_chunk = self.audio_queue.get()
                        
                # Flatten to a 1D array for easier processing if mono
                float_array = audio_chunk.flatten()
                        
                # --- Audio processing goes here ---
                # print the shape and current maximum amplitude
                # max_amplitude = np.max(np.abs(float_array))
                # print(f"Array Shape: {float_array.shape} | Max Amplitude: {max_amplitude:.4f}")
                            
                for i in range(settings["node_count"]):
                    self.push2Queues(float_array, i)

                self.log_and_print(float_array)

                return float_array
            
        except Exception as e:
            print(f"An error occurred: {e}")