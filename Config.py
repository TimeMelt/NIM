"""
    Configuration File
    ===================

    - configuration file to manage various settings
        - circuit parameters
        - threading
        - queues
        - logging

"""

import pennylane as qml

# training weights and data
weights = [[0.25, 0.5, 1.0]]
data = None  # no values uses superposition to generate random values, if values are needed structure like [[0, 0.1, 0.2, etc]]

# quantum circuit config
n_wires = 3     # number of qubits/wires
n_shots = 1000  # number of shots
epochs = None   # number of epochs loops - (set to None for infinte loop)

# define device/qpu
device = qml.device("default.mixed", wires=n_wires)

# number of inceptron instances to spin-up
node_count = 3

# logs directory
log_dir = "logs"

# delay for threading and logging
thread_delay = 1
loop_delay = 1

# queue config
queue_address = '127.0.0.1'
queue_port = 5000
queue_authkey = b'password'

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
}