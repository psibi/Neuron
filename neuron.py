#!/usr/bin/python
import os
import os.path
import sys
import gtk
import pygtk
import dbm
import shlex
import shutil
import subprocess
from select_network import selectbpn_window
from adv_train import adv_train
from cnetwork import cnetwork
from qprop import qprop
from rprop import rprop

class Neuron_TextViewOutput:
    def __init__(self,textview):
        self.ntextview=textview

    def write(self,string):
        buf=self.ntextview.get_buffer()
        textiter=buf.get_end_iter()
        buf.insert(textiter,string+'\n\n')
        self.ntextview.set_buffer(buf)

class neuron:
    """Main Neuron Application"""
    def __init__(self):
        gladefile="./gui/neuron.xml"
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
        self.talgo_window=builder.get_object("talgo_window")
        self.incremental=builder.get_object("incremental")
        self.batch=builder.get_object("batch")
        self.rprop=builder.get_object("rprop")
        self.qprop=builder.get_object("qprop")
        self.algorithm=False
        self.algorithm_name=""
        self.filename=""
        self.loadfile=""
        self.rpropw=None
        self.qpropw=None
        sys.stdout=Neuron_TextViewOutput(self.ntextview)
        builder.connect_signals(self)
        self.aboutdialog.connect("response", lambda d,r: d.hide())
        self.cwindow=cnetwork()
 
    def write_neuron(self,string):
        buf=self.ntextview.get_buffer()
        textiter=buf.get_end_iter()
        buf.insert(textiter,string+'\n\n')
        self.ntextview.set_buffer(buf)
            
    def on_mainwindow_destroy(self,widget,data=None):
        gtk.main_quit()

    def on_Quit_activate(self,widget,data=None):
        gtk.main_quit()
        
    def on_algorithm_changed(self,radiomenuitem,data=None):
        """This function is called whenever the radiomenuitem state is changed. This sets the algorithm of the training network"""
        if self.algo_inc.get_active():
            self.algorithm_name="FANN_TRAIN_INCREMENTAL"
            self.incremental.set_active(True)
            self.algorithm=True
        elif self.algo_batch.get_active():
            self.algorithm_name="FANN_TRAIN_BATCH"
            self.batch.set_active(True)
            self.algorithm=True
        elif self.algo_rprop.get_active():
            self.algorithm_name="FANN_TRAIN_RPROP"
            self.rprop.set_active(True)
            if self.rpropw==None:
                self.rpropw=rprop()
                self.qpropw=None
            self.algorithm=True
        elif self.algo_qprop.get_active():
            self.algorithm_name="FANN_TRAIN_QUICKPROP"
            self.qprop.set_active(True)
            if self.qpropw==None:
                self.qpropw=qprop()
                self.rpropw=None
            self.algorithm=True
        db=dbm.open('config.dat','c')
        db['Training Algorithm']=self.algorithm_name
        db.close()

    def on_algorithm_selected(self,radiomenuitem,data=None):
        if self.incremental.get_active():
            self.algo_inc.set_active(True)
        elif self.batch.get_active():
            self.algo_batch.set_active(True)
        elif self.rprop.get_active():
            self.algo_rprop.set_active(True)
            if self.rpropw==None:
                self.rpropw=rprop()
                self.qpropw=None
        elif self.qprop.get_active():
            self.algo_qprop.set_active(True)
            if self.qpropw==None:
                self.qpropw=qprop()
                self.rpropw=None

    def on_talgo_window_delete_event(self,widget,data=None):
        self.talgo_window.hide()
        return True

    def on_selectnetwork(self,widget,data=None):
        sel_win=selectbpn_window()

    def on_about_menuitem_activate(self,widget,data=None):
        self.aboutdialog.show()

    def get_training_data(self,widget,data=None):
        self.fcdialog.show()

    def on_fc_cancel(self,widget,data=None):
        self.fcdialog.hide()

    def on_fc_ok(self,widget,data=None):
        self.filename=self.fcdialog.get_filename()
        self.fcdialog.hide()
        if self.filename.endswith(".train"):
            db=dbm.open('config.dat','c')
            db['Training File']=self.filename
            db.close()
        elif self.filename.endswith(".test"):
            db=dbm.open('config.dat','c')
            db['Test File']=self.filename
            db.close()
        elif self.filename.endswith(".fa"):
            db=dbm.open('config.dat','c')
            db['Argument Data']=self.filename
            db.close()
        
    def start_training(self,widget,data=None):
        cmd="./train.py -t"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])
            
    def on_clean(self,widget,data=None):
        if os.path.isfile('config.dat.db'):
            os.remove('config.dat.db')
            dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"Neuron Dataset Cleaned")
            dlg.run()
            dlg.destroy()
        else:
            dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Neuron Dataset already Clean")
            dlg.run()
            dlg.destroy()

    def on_print(self,widget,data=None):
        if os.path.isfile('config.dat.db'):
            db=dbm.open('config.dat','c')
            for key in db.keys():
                line=key+"\t"+db[key]
                self.write_neuron(line)
            db.close()
        else:
            dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Neuron Dataset is empty.")
            dlg.run()
            dlg.destroy()

    def on_load(self,widget,data=None):
        self.fcdialog.show()

    def on_algorithm_clicked(self,widget,data=None):
        self.talgo_window.show()
        self.incremental.toggled()

    def on_talgo_ok_button_clicked(self,widget,data=None):
        self.talgo_window.hide()

    def on_cleantext_click(self,widget,data=None):
        buf=gtk.TextBuffer()
        buf.set_text("")
        self.ntextview.set_buffer(buf)

    def get_argument_data(self,widget,data=None):
        self.fcdialog.show()
         
    def approximate(self,widget,data=None):
        cmd="./fapprox.py"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])

    def get_test_data(self,widget,data=None):
        self.fcdialog.show()

    def on_test(self,widget,data=None):
        cmd="./test.py"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])

    def on_train_config_activate(self,widget,data=None):
        atrain=adv_train()
        atrain.show()

    def on_configure_menuitem_activate(self,widget,data=None):
        self.cwindow.show()

    def on_aboutdialog_delete_event(self,widget,data=None):
        self.aboutdialog.hide()
        return True
    
    def on_training_filechooser_delete_event(self,widget,data=None):
        self.fcdialog.hide()
        return True

if __name__=="__main__":
    neuron_window=neuron()
    gtk.main()
