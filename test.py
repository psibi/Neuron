#!/usr/bin/python
from pyfann import libfann
import dbm
import sys

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
db.close()

class function_aprox:

    def __init__(self):
        self.ann = libfann.neural_net()
        
    def test(self):
        self.ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
        self.ann.set_learning_rate(learning_rate)
        self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        self.ann.train_on_file(tfile, max_iterations, iterations_between_reports, desired_error)
        print "\nFunction Approximation Details:"
        fin=open("./dataset/xor.fa","r")
        print ""
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


