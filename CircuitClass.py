"""
    Quantum Circuit
    ================

    This is the circuit that is fed into and ran within each Inceptron object
        - this is the circuit that is being trainied/optimized
        - state prep:
            - when using data to optimize, Angle Embedding is used for state prep
                - must be integer or float values
                - this method would mimic the same concept of using training data on conventional neural networks
            - when not using data to optimize than each qubit/wire is set to an arbitrary superposition
"""

import pennylane as qml
import threading
from sensory_units.AudioStreamClass import AudioStream

def grab_audio():
    stream = AudioStream()
    output = stream.return_value()
    return output

class Circuit(threading.Thread):
    def __init__(self, device, n_wires, n_shots):
        super().__init__()
        self.device = device
        self.n_wires = n_wires
        self.n_shots = n_shots

    def run(self, weights, data):
        @qml.qnode(self.device)
        def inceptron(self, weights, data):
            if data is not None:
                if data is "audio":
                    audio = grab_audio()
                    audio_crumbs = audio[:self.n_wires]  # grab values from beginning of array to fit number of qubits/wires
                    qml.AngleEmbedding(features=audio_crumbs, wires=range(self.n_wires), rotation='Z')
                else:
                    qml.AngleEmbedding(features=data, wires=range(self.n_wires), rotation='Z')
            for i in range(self.n_wires):
                if data is None:
                    qml.Hadamard(wires=i)
                for j in range(len(weights)):
                    qml.RX(weights[j][0], wires=i)
                    qml.RY(weights[j][1], wires=i)
                    qml.RZ(weights[j][2], wires=i)
            return [qml.expval(qml.PauliZ(n)) for n in range(self.n_wires)]
        return inceptron(self, weights, data)