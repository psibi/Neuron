#!/usr/bin/python
# Copyright (C) 2012 Sibi <sibi@psibi.in>
#
# This file is part of Neuron.
#
# Neuron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Neuron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Neuron.  If not, see <http://www.gnu.org/licenses/>.
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
    num_neurons_hidden=db['Hidden Neurons']
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
    """Class for training the BPN Network."""
    def __init__(self):
        print "Training Initialization taking place\n"
        self.ann = libfann.neural_net()
        self.network_file=""

    def train(self):
        """Trains the BPN network."""
        db=dbm.open('config.dat','c')
        connection_rate=float(db['Connection Rate'])
        learning_rate=float(db['Learning Rate'])
        desired_error=float(db['Desired Error'])
        max_iterations=int(db['Maximum Iterations'])
        iterations_between_reports=int(db['Iteration Between Reports'])
        ol_act_fun=db['Output Layer Activation Function']
        db.close()
        hidden_neurons_list = [num_input]
        lay_neurons = tuple(num_neurons_hidden.split(",")) #Hidden Neurons in String
        for hid_neuron in lay_neurons:
            hidden_neurons_list.append(int(hid_neuron))
        hidden_neurons_list.append(num_output)
        hnt = tuple(hidden_neurons_list)            
        hiddenn = num_neurons_hidden.split(",")
        if bpn_type=="SPR":
            self.ann.create_sparse_array(connection_rate, hnt)
        elif bpn_type=="STD":
            self.ann.create_standard_array(hnt)
        elif bpn_type=="SRT":
            self.ann.create_shortcut_array(hnt)
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
        if ol_act_fun=="LINEAR":
            self.ann.set_activation_function_output(libfann.LINEAR)
        elif ol_act_fun=="THRESHOLD":
            self.ann.set_activation_function_output(libfann.THRESHOLD)
        elif ol_act_fun=="THRESHOLD SYMMETRIC":
            self.ann.set_activation_function_output(libfann.THRESHOLD_SYMMETRIC)
        elif ol_act_fun=="SIGMOID":
            self.ann.set_activation_function_output(libfann.SIGMOID)
        elif ol_act_fun=="SIGMOID STEPWISE":
            self.ann.set_activation_function_output(libfann.SIGMOID_STEPWISE)
        elif ol_act_fun=="SIGMOID SYMMETRIC":
            self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC)
        elif ol_act_fun=="GAUSSIAN":
            self.ann.set_activation_function_output(libfann.GAUSSIAN)
        elif ol_act_fun=="GAUSSIAN SYMMETRIC":
            self.ann.set_activation_function_output(libfann.GAUSSIAN_SYMMETRIC)
        elif ol_act_fun=="ELLIOT":
            self.ann.set_activation_function_output(libfann.ELLIOT)
        elif ol_act_fun=="ELLIOT SYMMETRIC":
            self.ann.set_activation_function_output(libfann.ELLIOT_SYMMETRIC)
        elif ol_act_fun=="LINEAR PIECE":
            self.ann.set_activation_function_output(libfann.LINEAR_PIECE)
        elif ol_act_fun=="LINEAR PIECE SYMMETRIC":
            self.ann.set_activation_function_output(libfann.LINEAR_PIECE_SYMMETRIC)
        elif ol_act_fun=="SIN SYMMETRIC":
            self.ann.set_activation_function_output(libfann.SIN_SYMMETRIC)
        elif ol_act_fun=="COS SYMMETRIC":
            self.ann.set_activation_function_output(libfann.COS_SYMMETRIC)
        elif ol_act_fun=="SIN":
            self.ann.set_activation_function_output(libfann.SIN)
        elif ol_act_fun=="COS":
            self.ann.set_activation_function_output(libfann.COS)
        elif ol_act_fun=="SIGMOID SYMMETRIC STEPWISE":
            self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
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
            elif af_n=="THRESHOLD":
                self.ann.set_activation_function(libfann.THRESHOLD,layer_no,neuron_no)
            elif af_n=="THRESHOLD SYMMETRIC":
                self.ann.set_activation_function(libfann.THRESHOLD_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="SIGMOID":
                self.ann.set_activation_function(libfann.SIGMOID,layer_no,neuron_no)
            elif af_n=="SIGMOID STEPWISE":
                self.ann.set_activation_function(libfann.SIGMOID_STEPWISE,layer_no,neuron_no)
            elif af_n=="SIGMOID SYMMETRIC":
                self.ann.set_activation_function(libfann.SIGMOID_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="GAUSSIAN":
                self.ann.set_activation_function(libfann.GAUSSIAN,layer_no,neuron_no)
            elif af_n=="GAUSSIAN SYMMETRIC":
                self.ann.set_activation_function(libfann.GAUSSIAN_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="ELLIOT":
                self.ann.set_activation_function(libfann.ELLIOT,layer_no,neuron_no)
            elif af_n=="ELLIOT SYMMETRIC":
                self.ann.set_activation_function(libfann.ELLIOT_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="LINEAR PIECE":
                self.ann.set_activation_function(libfann.LINEAR_PIECE,layer_no,neuron_no)
            elif af_n=="LINEAR PIECE SYMMETRIC":
                self.ann.set_activation_function(libfann.LINEAR_PIECE_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="SIN SYMMETRIC":
                self.ann.set_activation_function(libfann.SIN_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="COS SYMMETRIC":
                self.ann.set_activation_function(libfann.COS_SYMMETRIC,layer_no,neuron_no)
            elif af_n=="SIN":
                self.ann.set_activation_function(libfann.SIN,layer_no,neuron_no)
            elif af_n=="COS":
                self.ann.set_activation_function(libfann.COS,layer_no,neuron_no)
            if af_l=="LINEAR":
                self.ann.set_activation_function_layer(libfann.LINEAR,af_layer_number)
            elif af_l=="THRESHOLD":
                self.ann.set_activation_function(libfann.THRESHOLD,layer_no,neuron_no)
            elif af_l=="THRESHOLD SYMMETRIC":
                self.ann.set_activation_function(libfann.THRESHOLD_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="SIGMOID":
                self.ann.set_activation_function(libfann.SIGMOID,layer_no,neuron_no)
            elif af_l=="SIGMOID STEPWISE":
                self.ann.set_activation_function(libfann.SIGMOID_STEPWISE,layer_no,neuron_no)
            elif af_l=="SIGMOID SYMMETRIC":
                self.ann.set_activation_function(libfann.SIGMOID_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="GAUSSIAN":
                self.ann.set_activation_function(libfann.GAUSSIAN,layer_no,neuron_no)
            elif af_l=="GAUSSIAN SYMMETRIC":
                self.ann.set_activation_function(libfann.GAUSSIAN_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="ELLIOT":
                self.ann.set_activation_function(libfann.ELLIOT,layer_no,neuron_no)
            elif af_l=="ELLIOT SYMMETRIC":
                self.ann.set_activation_function(libfann.ELLIOT_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="LINEAR PIECE":
                self.ann.set_activation_function(libfann.LINEAR_PIECE,layer_no,neuron_no)
            elif af_l=="LINEAR PIECE SYMMETRIC":
                self.ann.set_activation_function(libfann.LINEAR_PIECE_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="SIN SYMMETRIC":
                self.ann.set_activation_function(libfann.SIN_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="COS SYMMETRIC":
                self.ann.set_activation_function(libfann.COS_SYMMETRIC,layer_no,neuron_no)
            elif af_l=="SIN":
                self.ann.set_activation_function(libfann.SIN,layer_no,neuron_no)
            elif af_l=="COS":
                self.ann.set_activation_function(libfann.COS,layer_no,neuron_no)
            self.ann.set_activation_steepness(svalue,layer,neuron)
            self.ann.set_activation_steepness_layer(vsteep,vslayer)
            if tef=="LINEAR":
                self.ann.set_train_error_function(libfann.ERRORFUNC_LINEAR)
            elif tef=="TANH ERROR FUNCTION":
                self.ann.set_train_error_function(libfann.ERRORFUNC_TANH)
            if tsf=="MSE":
                self.ann.set_train_stop_function(libfann.STOPFUNC_MSE)
            elif tsf=="BIT FAIL":
                self.ann.set_train_stop_function(libfann.STOPFUNC_BIT)
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
            cse=int(db['Candidate Stagnation Epochs'])
            wm=float(db['Weight Multiplier'])
            cl=float(db['Candidate Limit'])
            max_oe=int(db['Maximum Out Epochs'])
            min_oe=int(db['Minimum Out Epochs'])
            max_ce=int(db['Maximum Candidate Epochs'])
            min_ce=int(db['Minimum Candidate Epochs'])
            num_cgroup=int(db['Number Candidate Groups'])
            db.close()
            self.ann.set_cascade_output_change_fraction(ocf)
            self.ann.set_cascade_output_stagnation_epochs(ose)
            self.ann.set_cascade_candidate_change_fraction(ccf)
            self.ann.set_cascade_candidate_stagnation_epochs(cse)
            self.ann.set_cascade_weight_multiplier(wm)
            self.ann.set_cascade_candidate_limit(cl)
            self.ann.set_cascade_max_out_epochs(max_oe)
            #self.ann.set_cascade_min_out_epochs(min_oe)
            self.ann.set_cascade_max_cand_epochs(max_ce)
            #self.ann.set_cascade_min_cand_epochs(min_ce)
            self.ann.set_cascade_num_candidate_groups(num_cgroup)
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
        print "Neuron Network Also saved at "+ network_fname
        self.ann.save(self.network_file)
        print "\nBPN Network Connection:\n"
        self.ann.print_connections()
        self.move_network_file()

    def move_network_file(self):
        """Move the Network file under the dataset folder."""
        filename="./dataset/"+self.network_file
        if os.path.isfile(filename):
            os.remove(filename)
        src=self.network_file
        dest="./dataset/"
        shutil.move(src,dest)

if __name__=="__main__":
    network=bpn()
    network.train()


