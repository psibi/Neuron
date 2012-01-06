#!/usr/bin/python
from pyfann import libfann
import dbm
import sys
import gtk
import shutil
import os

try:
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
except KeyError as key:
    dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, str(key)+ " Uninitialized")
    dlg.run()
    dlg.destroy()
    db.close()
    sys.exit(1)
finally:
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
            self.ann.create_shortcut_array((num_input,num_neurons_hidden,num_output))
        if talgo=="FANN_TRAIN_INCREMENTAL":
            self.ann.set_training_algorithm(libfann.TRAIN_INCREMENTAL)
        elif talgo=="FANN_TRAIN_BATCH":
            self.ann.set_training_algorithm(libfann.TRAIN_BATCH)
        elif talgo=="FANN_TRAIN_RPROP":
            self.ann.set_training_algorithm(libfann.TRAIN_RPROP)
            try:
                db=dbm.open('config.dat','c')
                inc_factor=float(db['Increase Factor'])
                dec_factor=float(db['Decrease Factor'])
                delta_min=float(db['Delta Minimum'])
                delta_max=float(db['Delta Maximum'])
                delta_zero=float(db['Delta Zero'])
                db.close()
            except KeyError:
                pass
            else:
                self.ann.set_rprop_increase_factor(inc_factor)
                self.ann.set_rprop_decrease_factor(dec_factor)
                self.ann.set_rprop_delta_min(delta_min)
                self.ann.set_rprop_delta_max(delta_max)
        elif talgo=="FANN_TRAIN_QUICKPROP":
            self.ann.set_training_algorithm(libfann.TRAIN_QUICKPROP)
            try:
                db=dbm.open('config.dat','c')
                decay_val=float(db['Decay Value'])
                mu_val=float(db['Mu Value'])
                db.close()
            except KeyError:
                pass
            else:
                self.ann.set_quickprop_decay(decay_val)
                self.ann.set_quickprop_mu(mu_val)
        self.ann.set_learning_rate(learning_rate)
        if ol_act_fun=="SIGMODIAL FUNCTION":
            self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        elif ol_act_fun=="LINEAR FUNCTION":
            self.ann.set_activation_function_output(libfann.LINEAR)
        self.ann.train_on_file(tfile, max_iterations, iterations_between_reports, desired_error)
        fileparts=tfile.split('/')
        fileparts.reverse()
        name=fileparts[0]
        temp=name.split('.')
        self.network_file=temp[0]+".net"
        network_fname="./dataset/"+temp[0]+".net"
        self.ann.print_parameters()
        print "Neuron Network Also saved at "+ network_fname
        self.ann.save(self.network_file)
        self.move_network_file()

    def move_network_file(self):
        filename="./dataset/"+self.network_file
        if os.path.isfile(filename):
            os.remove(filename)
        src=self.network_file
        dest="./dataset/"
        shutil.move(src,dest)

if __name__=="__main__":
    network=bpn()
    network.train()

        
