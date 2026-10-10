"""
    Configuration File
    ===================

    - configuration file to manage various settings
        - circuit parameters
        - threading
        - queues
        - logging
        - audio input

"""

import pennylane as qml

# training weights and data
#   data=None uses superposition to generate random values, data="audio" pulls live data from microphone, 
#   data="screen-capture" pulls live data from device monitor/screen
#   if values are needed structure like data=[[0, 0.1, 0.2, etc]]
weights = [[0.25, 0.5, 1.0]]
data = "screen-capture"  

# quantum circuit config
n_wires = 3     # number of qubits/wires, screen-capture usage requires multiples of 3
n_shots = 1000  # number of shots
epochs = None   # number of epochs loops - (set to None for infinte loop)

# optimizer config
bandwidth = len(weights[0])
n_components = len(weights[0])

# define device/qpu
device = qml.device("default.mixed", wires=n_wires)

# number of inceptron instances to spin-up
node_count = 3

# logs directory
log_dir = "logs"

# delay for threading and logging
thread_delay = 1  # startup delay for inceptron threads
loop_delay = 0  # delay for inceptron execution loop (highly recommended to be set to 0 if data="audio")

# queue config
queue_address = '127.0.0.1'
queue_port = 5000
queue_authkey = b'password'

# audio input config
SAMPLE_RATE = 44100  # CD quality audio (Hz)
CHANNELS = 1         # 1 for mono, 2 for stereo
BLOCK_SIZE =  1024    # Number of frames per buffer chunk (default 1024)

# export and reference configurations using dictionary
settings = {
    "weights": weights,
    "n_wires": n_wires,
    "n_shots": n_shots,
    "epochs": epochs,
    "device": device,
    "node_count": node_count,
    "data": data,
    "log_dir": log_dir,
    "thread_delay": thread_delay,
    "loop_delay": loop_delay,
    "queue_address": queue_address,
    "queue_port": queue_port,
    "queue_authkey": queue_authkey,
    "audio_sample_rate": SAMPLE_RATE,
    "audio_channel_number": CHANNELS,
    "audio_block_size": BLOCK_SIZE,
    "bandwidth": bandwidth,
    "n_components": n_components,
}