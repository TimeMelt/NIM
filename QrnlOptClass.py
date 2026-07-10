"""
    QRNL - Quantum Circuit Optimizer
    =================================
    
    - uses machine learning to optimize circuits
        - optimizer learns alongside circuits
        - uses sklearn machine learning (not neural networks)
    - consists of models listed below
        - Kernel Density Model
            - take 1 sample from Kernel Density model and feed it to
              Restricted Boltzmann Machine
        - Restricted Boltzmann Machine
            - for 1st optimization round/epoch, model does normal fit, for 
              subsequent rounds/epochs model does partial fit
            - partial fit feature allows optimizer to learn alongside circuits
    - adjusting parameters of each model within QRNL optimizer class allows for adjustment 
      of optimization 
"""

from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import KernelDensity

class QRNL:
    def __init__(self, kernel='gaussian', bandwidth=3, n_components=3, learning_rate=0.1, batch_size=10 ,n_iter=10):
        self.dry = True
        self.kde = KernelDensity(kernel=kernel, bandwidth=bandwidth)
        self.rbmq = BernoulliRBM(n_components=n_components, learning_rate=learning_rate, batch_size=batch_size ,n_iter=n_iter) #defaults: learning_rate=0.1, batch_size=10 ,n_iter=10

    def fit(self,weights):
        self.kde.fit(weights)
        sample = self.kde.sample(1)
        if self.dry is True:
            self.rbmq.fit(weights)
            self.dry = False
        else:
            self.rbmq.partial_fit(weights)
        return self.rbmq.transform(sample)
