#!/usr/bin/python
from pyfann import libfann
import dbm
import sys
import gtk
import shutil

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
    test_file=db['Test File']
except KeyError as key:
    dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, str(key)+ " Uninitialized")
    dlg.run()
    dlg.destroy()
    db.close()
    sys.exit(1)
finally:
    db.close()

class bpn_test:

    def __init__(self):
        pass

    def test(self):
        print "Creating network."	
        train_data = libfann.training_data()
        train_data.read_train_from_file(tfile)
        ann = libfann.neural_net()
        if bpn_type=="SPR":
            ann.create_sparse_array(connection_rate, (len(train_data.get_input()[0]), num_neurons_hidden, len(train_data.get_output()[0])))
        elif bpn_type=="STD":
            ann.create_standard_array((len(train_data.get_input()[0]), num_neurons_hidden, len(train_data.get_output()[0])))
        elif bpn_type=="SRT":
            ann.create_shortcut_array((len(train_data.get_input()[0]), num_neurons_hidden, len(train_data.get_output()[0])))
        ann.set_learning_rate(learning_rate)
        if talgo=="FANN_TRAIN_INCREMENTAL":
            ann.set_training_algorithm(libfann.TRAIN_INCREMENTAL)
        elif talgo=="FANN_TRAIN_BATCH":
            ann.set_training_algorithm(libfann.TRAIN_BATCH)
        elif talgo=="FANN_TRAIN_RPROP":
            ann.set_training_algorithm(libfann.TRAIN_RPROP)
        elif talgo=="FANN_TRAIN_QUICKPROP":
            ann.set_training_algorithm(libfann.TRAIN_QUICKPROP)
	ann.train_on_data(train_data, max_iterations, iterations_between_reports, desired_error)
        print "Testing network"
        test_data = libfann.training_data()
        test_data.read_train_from_file(test_file)
        ann.reset_MSE()
        ann.test_data(test_data)
        print "MSE error on test data: %f" % ann.get_MSE()

if __name__=="__main__":
    network=bpn_test()
    network.test()

        
