#!/usr/bin/python
import sys
import gtk
import pygtk
import dbm
import shlex
import subprocess
from select_network import selectbpn_window

class neuron:
    """Main Neuron Application"""
    def __init__(self):
        gladefile="neuron.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("mainwindow")
        self.fcdialog=builder.get_object("training_filechooser")
        self.algo_inc=builder.get_object("incremental_menuitem")
        self.algo_batch=builder.get_object("batch_menuitem")
        self.algo_rprop=builder.get_object("rprop_menuitem")
        self.algo_qprop=builder.get_object("qprop_menuitem")
        self.aboutdialog=builder.get_object("aboutdialog")
        self.ntextview=builder.get_object("neuron_textview")
        self.algorithm=False
        self.algorithm_name=""
        builder.connect_signals(self)

    def write_neuron(self,string):
        buffer=gtk.TextBuffer()
        buffer.set_text(string)
        self.ntextview.set_buffer(buffer)
            
    def on_mainwindow_destroy(self,widget,data=None):
        gtk.main_quit()

    def on_Quit_activate(self,widget,data=None):
        gtk.main_quit()
        
    def on_algorithm_changed(self,radiomenuitem,data=None):
        """This function is called whenever the radiomenuitem state is changed. This sets the algorithm of the training network"""
        if self.algo_inc.get_active():
            self.algorithm_name="FANN_TRAIN_INCREMENTAL"
            self.algorithm=True
        elif self.algo_batch.get_active():
            self.algorithm_name="FANN_TRAIN_BATCH"
            self.algorithm=True
        elif self.algo_rprop.get_active():
            self.algorithm_name="FANN_TRAIN_RPROP"
            self.algorithm=True
        elif self.algo_qprop.get_active():
            self.algorithm_name="FANN_TRAIN_QUICKPROP"
            self.algorithm=True
           
    def on_selectnetwork(self,widget,data=None):
        db=dbm.open('config.dat','c')
        db['Algorithm']=self.algorithm_name
        db.close()
        sel_win=selectbpn_window()

    def on_about_menuitem_activate(self,widget,data=None):
        self.aboutdialog.show()

    def on_aboutdialog_destroy(self,widget,data=None):
        self.aboutdialog.hide()

    def get_training_data(self,widget,data=None):
        self.fcdialog.show()

    def on_fc_cancel(self,widget,data=None):
        self.fcdialog.hide()

    def on_fc_ok(self,widget,data=None):
        filename=self.fcdialog.get_filename()
        self.fcdialog.hide()

    def start_training(self,widget,data=None):
        cmd="./simple_train.py -t"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])

if __name__=="__main__":
    neuron_window=neuron()
    gtk.main()

