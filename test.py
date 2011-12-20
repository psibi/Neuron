#!/usr/bin/python
from pyfann import libfann

connection_rate = 1
learning_rate = 0.7
num_input = 2
num_neurons_hidden = 4
num_output = 1

desired_error = 0.0001
max_iterations = 100000
iterations_between_reports = 1000

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

ann.train_on_file("../../examples/xor.data", max_iterations, iterations_between_reports, desired_error)

fin=open("xor.fa","r")
inputs=fin.readlines()
fin.close()
width=10
once=True
#inp1=((1,-1),(-1,1))
for inp in inputs:
    a=inputs.pop()
    b=a.split(' ')
    sample=b[1]
    second=sample[:-1]
    #print b
    inpu=(int(b[0]),int(second))
    calc_out=ann.run(inpu)
    i=""
    header=""
    for x in range(len(inpu)):
        i=i+" "+str(inpu[x]).ljust(9)
        header=header+" "+"Input #"+str(x)
        header.rjust(width)
    if once:
        print header+" ","Approximated Value"
        once=False
    print i+" ",calc_out
