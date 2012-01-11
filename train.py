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
        db=dbm.open('config.dat','c')
        connection_rate=float(db['Connection Rate'])
        learning_rate=float(db['Learning Rate'])
        desired_error=float(db['Desired Error'])
        max_iterations=int(db['Maximum Iterations'])
        iterations_between_reports=int(db['Iteration Between Reports'])
        ol_act_fun=db['Output Layer Activation Function']
        db.close()
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
        #For Advanced Parameters related to Fixed Topology
        try:
            db=dbm.open('config.dat','c')
            lmomentum=float(db['Learning Momentum'])
            af_neuron_number=db['AF for Neuron']
            af_n=db['AF Neuron']
            af_layer_number=int(db['AF for layer'])
            af_l=db['AF Layer']
            asn=db['Activation Steepness for Neuron']
            asl=db['Activation Steepness for layer']
            tef=db['Train Error Function']
            tsf=db['Train Stop Function']
            bfl=float(db['Bit Fail Limit'])
            db.close()
        except KeyError:
            pass
        else:
            self.ann.set_learning_momentum(lmomentum)
            temp_list=af_neuron_number.split(",")
            layer_no=int(temp_list[0])
            neuron_no=int(temp_list[1])
            steepness_list=asn.split(",")
            svalue=float(steepness_list[0])
            layer=int(steepness_list[1])
            neuron=int(steepness_list[2])
            steep_layer_list=asl.split(",")
            vsteep=float(steep_layer_list[0])
            vslayer=int(steep_layer_list[1])
            if af_n=="LINEAR":
                self.ann.set_activation_function(libfann.LINEAR,layer_no,neuron_no)
            if af_l=="LINEAR":
                self.ann.set_activation_function_layer(libfann.LINEAR,af_layer_number)
            self.ann.set_activation_steepness(svalue,layer,neuron)
            self.ann.set_activation_steepness_layer(vsteep,vslayer)
            if tef=="LINEAR":
                self.ann.set_train_error_function(libfann.ERRORFUNC_LINEAR)
            if tsf=="MSE":
                self.ann.set_train_stop_function(libfann.STOPFUNC_MSE)
            self.ann.set_bit_fail_limit(bfl)
        finally:
            db.close()
        #Find Out Whether it is Evolving topology or Fixed Topology
        try:
            db=dbm.open('config.dat','c')
            max_neurons=db['Maximum Neurons']
            ncascade=True
            db.close()
        except KeyError:
            ncascade=False
        finally:
            db.close()
        if ncascade:
            db=dbm.open('config.dat','c')
            max_neurons=int(db['Maximum Neurons'])
            neurons_between_reports=int(db['Neurons Between Reports'])
            cdesired_error=float(db['Desired Error'])
            db.close()
        #For Advanced Cascade Parameters
        try:
            db=dbm.open('config.dat','c')
            ocf=db['Output Change Fraction']
            db.close()
            tcascade=True
        except KeyError:
            tcascade=False

        if tcascade:
            db=dbm.open('config.dat','c')
            ocf=float(db['Output Change Fraction'])
            ose=int(db['Output Stagnation Epochs'])
            ccf=float(db['Candidate Change Fraction'])
            cse=float(db['Candidate Stagnation Epochs'])
            wm=float(db['Weight Multiplier'])
            cl=float(db['Candidate Limit'])
            max_oe=int(db['Maximum Out Epochs'])
            min_oe=int(db['Minimum Out Epochs'])
            max_ce=int(db['Maximum Candidate Epochs'])
            min_ce=int(db['Minimum Candidate Epochs'])
            db.close()
            self.ann.set_cascade_output_change_fraction(ocf)
            self.ann.set_cascade_output_stagnation_epochs(ose)
            self.ann.set_cascade_candidate_change_fraction(ccf)
            self.ann.set_cascade_candidate_stagnation_epochs(cse)
            self.ann.set_cascade_weight_multiplier(wm)
            self.ann.set_cascade_candidate_limit(cl)
            self.ann.set_cascade_max_out_epochs(max_oe)
            self.ann.set_cascade_min_out_epochs(min_oe)
            self.ann.set_cascade_max_cand_epochs(max_ce)
            self.ann.set_cascade_min_cand_epochs(min_ce)
        if ncascade:
            self.ann.cascadetrain_on_file(tfile,max_neurons,neurons_between_reports,cdesired_error)
        else:
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
