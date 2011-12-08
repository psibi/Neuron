import sys
import gtk
import pygtk

#!/usr/bin/python
class neuron:
    """Main Neuron Application"""
    def __init__(self):
        gladefile="neural.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("mainwindow")
        self.algo_inc=builder.get_object("incremental_menuitem")
        self.algo_batch=builder.get_object("batch_menuitem")
        self.algo_rprop=builder.get_object("rprop_menuitem")
        self.algo_qprop=builder.get_object("qprop_menuitem")
        self.algorithm=False
        self.algorithm_name=""
        builder.connect_signals(self)

    def on_mainwindow_destroy(self,widget,data=None):
        gtk.main_quit()

    def on__Quit_activate(self,widget,data=None):
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
            self.algorithm=False
            
if __name__=="__main__":
    neuron_window=neuron()
    gtk.main()


        
