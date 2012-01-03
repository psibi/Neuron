#!/usr/bin/python
from pyfann import libfann
import dbm
import sys
import gtk

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
    afile=db['Argument Data']
except KeyError as key:
    dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, str(key)+ " Uninitialized")
    dlg.run()
    dlg.destroy()
    db.close()
    sys.exit(1)
finally:
    db.close()

class function_aprox:
    
    def __init__(self):
        self.ann = libfann.neural_net()
        
    def test(self):
        print "BPN Network Training Details:\n"
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
        if ol_act_fun=="SIGMODIAL FUNCTION":
            self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        elif ol_act_fun=="LINEAR FUNCTION":
            self.ann.set_activation_function_output(libfann.LINEAR)
        self.ann.train_on_file(tfile, max_iterations, iterations_between_reports, desired_error)
        print "\nFunction Approximation Details:"
        fin=open(afile,"r")
        inputs=fin.readlines()
        fin.close()
        width=20
        once=True
        for ite in range(len(inputs)):
            a=inputs.pop()
            b=a.split(' ')
            sample=b[1]
            second=sample[:-1]
            inpu=(int(b[0]),int(second))
            calc_out=self.ann.run(inpu)
            i=""
            header=""
            for x in range(len(inpu)):
                i=i+"\t"+str(inpu[x]).ljust(width)
                header=header+"\t"+"Input #"+str(x)
                header.rjust(width)
            if once:
                print header+" ","Approximated Value"
                once=False
            print i+"\t",calc_out

if __name__=="__main__":
    network=function_aprox()
    network.test()


