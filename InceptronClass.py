"""
    Inceptron Class
    ================

    This node is what allows circuits to send optimized weights to each-other in a mesh/queue format. 
        - this mesh interaction allows for circuits to learn from eachother in an interconnected format
          (like the brain of an organisim)
    - runs each circuit instance
    - contains queue to manage incoming optimized weights from other circuits in the network
        - all inceptrons in a mesh feed into eachothers queues 
"""

import pennylane as qml
from QrnlOptClass import QRNL
import time, logging
from multiprocessing.managers import BaseManager
import threading
from CircuitClass import Circuit
from Config import settings

class QueueManager(BaseManager): pass

class Inceptron(threading.Thread):
    def __init__(self, n_wires, n_shots, epochs, device, placement, queue_manager, node_count, circuit, data):
        super().__init__()
        self.queue_manager = queue_manager
        self.queue = [getattr(self.queue_manager, f"get_queue_{_}") for _ in range(node_count)]
        self.n_wires = n_wires
        self.n_shots = n_shots
        self.epochs = epochs
        self.device = device
        self.optimizer = QRNL()
        self.placement = placement
        self.circuit = circuit
        self.data = data

    def runCircuit(self, weigh):
        return self.circuit.run(weigh, self.data)
    

    # execute circuit and run QRNL optimizer
    # returns optimized weights and expectation values
    def circuitRunAndOpt(self, weigh):
        circuit_expval = self.runCircuit(weigh)
        optimized_values = self.optimizer.fit([circuit_expval])
        return [optimized_values, circuit_expval]

    def log_and_print(self, opt_weights, orig_weights, circuit_expval):
        logging.basicConfig(filename=f"{settings['log_dir']}/inceptron{self.placement}.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
        logging.info(f"\n orig weights: {orig_weights} \n opt weights: {opt_weights} \n circuit expval: {circuit_expval}")
    
    # grab/pop next set of weights to optimize
    def grabFromQueue(self):
        temp = getattr(self.queue_manager, f"get_queue_{self.placement}")
        return temp

    # push optimized weights to remote queues
    def push2Queues(self, weights, i):
        setattr(self.queue_manager, f"get_queue_{i}", weights)

    def runIt(self):
        my_weights = self.grabFromQueue() 
        for i in range(len(self.queue)):
            if i != self.placement:
                opt_weights_expval = self.circuitRunAndOpt(my_weights)
                self.push2Queues(opt_weights_expval[0], i) 
                self.log_and_print(opt_weights_expval[0], my_weights, opt_weights_expval[1])
                if settings["loop_delay"] > 0:
                    time.sleep(settings["loop_delay"]) 
            else:
                pass 

    def run(self):
        if self.epochs is None:
            print(f"infinite epochs set for node {self.placement}")
            while True:
                self.runIt()
        else:
            print(f"{self.epochs} epochs set for node {self.placement}")
            for i in range(self.epochs):
                self.runIt()
            
                

if __name__ == "__main__":
    qml.set_shots(shots=settings["n_shots"]) # set number of shots
    for i in range(settings["node_count"]): # loop to register inceptron queues
        print(f"registering Queue {i}")
        QueueManager.register(f"get_queue_{i}")
    queue_manager = QueueManager(address=(settings["queue_address"], settings["queue_port"]), authkey=settings["queue_authkey"])
    inceptron_list = [None]*settings["node_count"]
    for i in range(settings["node_count"]): # initialize inceptrons
        circuit = Circuit(settings["device"], settings["n_wires"], settings["n_shots"])
        inceptron_list[i] = Inceptron(settings["n_wires"], settings["n_shots"], settings["epochs"], settings["device"], 
                                      i, queue_manager, settings["node_count"], circuit, settings["data"])
        init_weights_expval = inceptron_list[i].circuitRunAndOpt(settings["weights"])
        setattr(queue_manager, f"get_queue_{i}", init_weights_expval[0])
        inceptron_list[i].log_and_print(init_weights_expval[0], settings["weights"], init_weights_expval[1])
    for i in range(settings["node_count"]): # start inceptron threads
        inceptron_list[i].start()
        time.sleep(settings["thread_delay"])
       