#!/usr/bin/python
from pyfann import libfann
import dbm
import sys
import gtk
import shutil

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

class bpn:

    def __init__(self):
        print "Training Initialization taking place\n"
        self.ann = libfann.neural_net()
        self.network_file=""

    def train(self):
        if bpn_type=="SPR":
            self.ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
        elif bpn_type=="STD":
            self.ann.create_standard_array((num_input,num_neurons_hidden,num_output))
        elif bpn_type=="SRT":
            self.ann.create_standard_array((num_input,num_neurons_hidden,num_output))
        if talgo=="FANN_TRAIN_INCREMENTAL":
            self.ann.set_training_algorithm(libfann.TRAIN_INCREMENTAL)
        elif talgo=="FANN_TRAIN_BATCH":
            self.ann.set_training_algorithm(libfann.TRAIN_BATCH)
        elif talgo=="FANN_TRAIN_RPROP":
            self.ann.set_training_algorithm(libfann.TRAIN_RPROP)
        elif talgo=="FANN_TRAIN_QUICKPROP":
            self.ann.set_training_algorithm(libfann.TRAIN_QUICKPROP)
        self.ann.set_learning_rate(learning_rate)
        self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        self.ann.train_on_file(tfile, max_iterations, iterations_between_reports, desired_error)
        fileparts=tfile.split('/')
        fileparts.reverse()
        name=fileparts[0]
        temp=name.split('.')
        self.network_file=temp[0]+".net"
        network_fname="../"+temp[0]+".net"
        print "Neuron Network Also saved at "+ network_fname
        self.ann.save(self.network_file)
        self.move_network_file()

    def move_network_file(self):
        src=self.network_file
        dest="./dataset/"
        shutil.move(src,dest)

if __name__=="__main__":
    network=bpn()
    network.train()

        
