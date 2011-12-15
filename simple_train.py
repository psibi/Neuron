#!/usr/bin/python
from pyfann import libfann
import dbm
import sys
#db=dbm.open('config.dat','c')
#connection_rate=db['connrate']
#learning_rate=db['lrate']
#desired_error= db['derror']
#max_iterations= db['miter']
#iterations_between_reports=db['ireport']
#function=db['function']
#network=db['network']
#numl=db['numl']
#num_input=db['inputn']
#num_output=db['outputn']
#num_neurons_hidden=db['hiddenn']
#numh_layers=db['numh']
#db.close()
db=dbm.open('config.dat','c')
talgo=db['Training Algorithm']
bpn_type=db['Network Type']
numl=int(db['Number of Layers'])
num_input=int(db['Input Neurons'])
num_output=int(db['Output Neurons'])
num_neurons_hidden=int(db['Hidden Neurons'])
num_hlay=int(db['Number of Hidden Layers'])
connection_rate=float(db['Connection Rate'])
learning_rate=float(db['Learning Rate'])
desired_error=float(db['Desired Error'])
max_iterations=int(db['Maximum Iterations'])
iterations_between_reports=int(db['Iteration Between Reports'])
ol_act_fun=db['Output Layer Activation Function']
tfile=db['Training File']
db.close()
#connection_rate = 1
#learning_rate = 0.7
#num_input = 2
#num_neurons_hidden = 4
#num_output = 1
#desired_error = 0.0001
#max_iterations = 100000
#iterations_between_reports = 1000

class bpn:

    def __init__(self):
        print "Training Initialization taking place\n"
        self.ann = libfann.neural_net()
        for arg in sys.argv[1:]:
            if arg=="-t":
                self.train()
            elif arg=="-p":
                self.train()
                self.print_param()

    def train(self):
        self.ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
        self.ann.set_learning_rate(learning_rate)
        self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        self.ann.train_on_file(tfile, max_iterations, iterations_between_reports, desired_error)
        self.ann.save("xor_float.net")

    def print_param(self):
        lr=self.ann.get_learning_rate()
        print lr

if __name__=="__main__":
    network=bpn()

