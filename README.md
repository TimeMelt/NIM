# Neural Inception Mesh (aka. NIM)

## A new paradigm in quantum processing...

### What is it??
- This code is conceptual architecture enabling quantum circuits to be linked together through mesh style queues, this allows the circuits to learn from eachothers outputs using a new type of optimizer (QrnLOpt) powered by machine learning.
- This architecture intends to take the idea of neural network esque interconnection and reap the benefits for quantum computations. Each circuit learns from every other circuit within the mesh.

    #### Note: this network can be run in 2 loop modes
    - infinite loop: keeps mesh network running persistently until user stops program. This allows the network to constantly accept inputs, learn from them, and produce outputs. Essentially the network is allowed to be constantly learning and teaching like an 'organic' brain.
    - fixed loop: mesh network runs optimization loop for fixed number similar to how more conventional circuits and ai models function. 

### Basic Concepts
- circuit: quantum operation or set of operations to be trained/optimized, optimizer must be used for successful training
- optimizer: used to train quantum circuits, this code uses a new type of optimizer called 'QrnLOpt'
- queue: where circuit outputs are stored until circuit can process/learn from them, each circuit has its own queue instance.
- inceptron: object instance that allows circuits to send optimized weights to each-other in a mesh/queue format, all inceptrons in a mesh feed into eachothers queues, therefore circuits learn from every other circuit. For each individual circuit there is an inceptron instance.
- server: this object allows queues to be visible across multiple threads

### QrnLOpt...new optimizer??
- QrnLOpt is a new optimizer type that uses machine learning to train circuits
- The structure is a 2 step pipeline that starts with a kernel density matrix and finishes with a restricted boltzmann machine. Parameters for both the kernel density matrix and restricted boltzmann machine can be configured to customize the training process as needed.
- Each circuit/inceptron has its own QrnLOpt optimizer making each have its own machine learning model, for example the optimizer in circuit 1 is a seperate model from the optimizer for circuit 2. There are as many machine learning models as there are circuits/inceptrons.
- a new optimizer architecture was created in order to give each quantum circuit within the mesh more dynamic learning/optimizaton capabilities.
- for this repository the QrnLOpt optimizer learns from the expectation value outputs from the other circuits within the mesh

### Benefits??
- Ideally this new technique for quantum processing will allow for more effective error correction while using a fraction of the qubits/wires of other methods
- Could also help with the development of new AI architectures powered by quantum processing

### Sensory Units
- sensory input units allows the mesh to learn in real time from different live inputs
- currently 2 sensory inputs exist
    - audio: microphone input
    - screen-capture: screenshots of display

### Setup/Execution commands (installs pip packages/starts mesh program)

    pip install -r requirements.txt
    ./initMesh.sh

### Configuration
use Config.py to configure any of these...
- circuit parameters
- threading
- queues
- logging
- audio input

### Logging
- log files default location is the /logs folder
- when mesh is stopped and restarted the previous log files are deleted and the new logs take their place, make sure to backup any logs that you want to preserve the results for.
- files are numerical based on inceptron number starting from 0, so for example if there are 3 nodes then the log files will be inceptron0.log, inceptron1.log, and inceptron2.log
- log entries include timestamp, orignal weights grabbed from queue, optimized weights, and the expectation value to be placed in other queues

#### example log entry

    2026-01-01 11:37:01,916 - INFO - 
     orig weights: [[0.25, 0.5, 1.0]] 
     opt weights: [[0.67336617 0.67886147 0.69883006]] 
     circuit expval: [np.float64(-0.4794255386042028), np.float64(-0.4794255386042027), np.float64(-0.4794255386042027)]



### Credits

This repository uses [Pennylane](https://pennylane.ai/) for the quantum computing capabilities/simulation and [Scikit-Learn](https://scikit-learn.org/) to develop the custom optimizer.



##### This software is distrubuted under the MIT License