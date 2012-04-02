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
#
"""Main Neuron Module. Acts as controller of the Simulator."""
import os
import os.path
import sys
import gtk
import pygtk
import dbm
import shlex
import shutil
import subprocess
import gtkunixprint
from select_network import selectbpn_window
from adv_train import adv_train
from cnetwork import cnetwork
from qprop import qprop
from rprop import rprop
from cascade import cascade

class Neuron_TextViewOutput:
    """Class used for logging the output of
    the application to the Textview present in 
    the Neuron Window."""
    def __init__(self,textview):
        self.ntextview=textview

    def write(self,string):
        """Writes output to the end of the Textview."""
        buf=self.ntextview.get_buffer()
        textiter=buf.get_end_iter()
        buf.insert(textiter,string+'\n\n')
        self.ntextview.set_buffer(buf)

class neuron:
    """Main Neuron Simulator"""
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
        self.train_config=builder.get_object("train_config")
        self.evolving_train_config=builder.get_object("evolving_train_config")
        self.statusbar=builder.get_object("statusbar")
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
        """Appends output to the end of Textview."""
        buf=self.ntextview.get_buffer()
        textiter=buf.get_end_iter()
        buf.insert(textiter,string+'\n\n')
        self.ntextview.set_buffer(buf)
            
    def on_mainwindow_destroy(self,widget,data=None):
        """Quits Neuron on destroy event."""
        gtk.main_quit()

    def on_Quit_activate(self,widget,data=None):
        """Quits Neuron on selection Quit menuitem."""
        gtk.main_quit()
        
    def on_algorithm_changed(self,radiomenuitem,data=None):
        """This function is called whenever the radiomenuitem 
        state is changed. This sets the algorithm of the 
        training network."""
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
        """Handler when a radiobutton get's toggled."""
        if self.incremental.get_active():
            self.algo_inc.set_active(True)
        elif self.batch.get_active():
            self.algo_batch.set_active(True)
            
    def on_talgo_window_delete_event(self,widget,data=None):
        """Delete event handler for training algorithm window."""
        self.talgo_window.hide()
        return True

    def on_selectnetwork(self,widget,data=None):
        """A new window is created on selecting network."""
        sel_win=selectbpn_window()

    def on_about_menuitem_activate(self,widget,data=None):
        """Displays About dialog box when appropriate menuitem
        is selected."""
        self.aboutdialog.show()

    def get_training_data(self,widget,data=None):
        """File chooser dialog is shown for selecting training data."""
        self.fcdialog.show()

    def on_fc_cancel(self,widget,data=None):
        """Cancel button handler for file chooser."""
        self.fcdialog.hide()

    def on_fc_ok(self,widget,data=None):
        """Ok button clicked() handler for file chooser dialog."""
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
        """Training Code for the Neuron Network."""
        context_id = self.statusbar.get_context_id("Train Start")
        self.statusbar.push(context_id,"Training Activity Started")
        if not self._validate_pretraining():
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Input Incompatible with Training file.")
            dlg.run()
            dlg.destroy()
            return
        cmd="./train.py -t"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])
        context_id = self.statusbar.get_context_id("Train Stop")
        self.statusbar.push(context_id,"Training Activity Completed")
            
    def on_clean(self,widget,data=None):
        """For cleaning the Neuron dataset."""
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
        """For printing parameters of the Neuron dataset."""
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
        """Displays file chooser dialog for selecting different 
        files for the simulator."""
        self.fcdialog.show()

    def on_algorithm_clicked(self,widget,data=None):
        """Handler on Clicking algorithm tool item."""
        self.talgo_window.show()
        self.incremental.toggled()

    def on_talgo_ok_button_clicked(self,widget,data=None):
        """Handler for ok button in talgo window"""
        self.talgo_window.hide()
        if self.rprop.get_active():
            if self.rpropw==None:
                self.rpropw=rprop()
                self.qpropw=None
                self.algo_rprop.set_active(True)
        elif self.qprop.get_active():
            if self.qpropw==None:
                self.qpropw=qprop()
                self.rpropw=None
                self.algo_qprop.set_active(True)
        
    def on_cleantext_click(self,widget,data=None):
        """For cleaning the TextView in Neuron."""
        buf=gtk.TextBuffer()
        buf.set_text("")
        self.ntextview.set_buffer(buf)

    def get_argument_data(self,widget,data=None):
        """For displaying the file chooser dialog to get
        Argument data."""
        self.fcdialog.show()
         
    def _validate_pretraining(self):
        """Validates the input data(i/o and o/p neurons) with training file"""
        try:
            db=dbm.open('config.dat','c')
            num_input=int(db['Input Neurons'])
            num_output=int(db['Output Neurons'])
            tfile=db['Training File']
        except KeyError as key:
            dlg=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK, str(key)+ " Uninitialized")
            dlg.run()
            dlg.destroy()
            db.close()
        finally:
            db.close()
        fhandler = open(tfile,'r')
        fline = fhandler.readline().strip().split()
        fhandler.close()
        cinput_neurons = int(fline[1])
        coutput_neurons = int(fline[2])
        if cinput_neurons!=num_input:
            return False
        elif coutput_neurons!=num_output:
            return False
        else:
            return True

    def approximate(self,widget,data=None):
        """For Function Approximation in Neuron."""
        context_id = self.statusbar.get_context_id("Appr Start")
        self.statusbar.push(context_id,"Function Approximation Activity Started")
        if not self._validate_pretraining():
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Input Incompatible with Training file.")
            dlg.run()
            dlg.destroy()
            return
        cmd="./fapprox.py"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])
        context_id = self.statusbar.get_context_id("Appr End")
        self.statusbar.push(context_id,"Function Approximation Activity Completed")

    def get_test_data(self,widget,data=None):
        """For displaying the file chooser dialog to get
        Test data."""
        self.fcdialog.show()

    def on_test(self,widget,data=None):
        """For testing of the BPN network in Neuron."""
        context_id = self.statusbar.get_context_id("Test Start")
        self.statusbar.push(context_id,"Test Activity Started")
        if not self._validate_pretraining():
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Input Incompatible with Training file.")
            dlg.run()
            dlg.destroy()
            return
        cmd="./test.py"
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        output=process.communicate()
        if output[0]:
            self.write_neuron(output[0])
        context_id = self.statusbar.get_context_id("Test Stop")
        self.statusbar.push(context_id,"Test Activity Completed")

    def on_train_config_activate(self,widget,data=None):
        """Handler to show window related to Advanced training
        of the simulator."""
        atrain=adv_train()
        atrain.show()

    def on_configure_menuitem_activate(self,widget,data=None):
        """For displaying the configure window."""
        self.cwindow.show()

    def on_aboutdialog_delete_event(self,widget,data=None):
        """Handler for the delete event on About dialog."""
        self.aboutdialog.hide()
        return True
    
    def on_training_filechooser_delete_event(self,widget,data=None):
        """Handler for the delete event of filechooser dialog."""
        self.fcdialog.hide()
        return True

    def on_evolving_train_config_activate(self,radiobutton,data=None):
        """For showing window for configuring parameters related to cascade
        Training."""
        wcascade=cascade()

    def on_save(self,widget,data=None):
        """Handler on pressing the save button on tool button"""
        dialog=gtk.FileChooserDialog("Save As",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK),None)
        response=dialog.run()
        if response==gtk.RESPONSE_OK:
            filename=dialog.get_filename()
            if filename.endswith(".pdf"):
                fileparts=filename.split(".")
                save_file=open(fileparts[0],'w')
                textbuffer=self.ntextview.get_buffer()
                startiter, enditer = textbuffer.get_bounds()
                text=textbuffer.get_text(startiter,enditer,False)
                if text=="":
                    dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Nothing to Print")
                    dlg.run()
                    dlg.destroy()
                    return
                save_file.write(text)
                save_file.close()
                cmd="./lib/pyText2pdf.py " + fileparts[0]
                args=shlex.split(cmd)
                process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
            else:
                save_file=open(filename,'w')
                textbuffer=self.ntextview.get_buffer()
                startiter, enditer = textbuffer.get_bounds()
                text=textbuffer.get_text(startiter,enditer,False)
                save_file.write(text)
                save_file.close()
        dialog.destroy()

    def print_cb(self,printjob, data, errormsg):
        if errormsg:
            print('Error occurred while printing:\n%s' % errormsg)

    def on_printing(self,widget,data=None):
        """Handler for printing files. Currently only supports UNIX platform"""
        save_file=open('temp','w')
        textbuffer=self.ntextview.get_buffer()
        startiter, enditer = textbuffer.get_bounds()
        text=textbuffer.get_text(startiter,enditer,False)
        if text=="":
            dlg=gtk.MessageDialog(self.window,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Nothing to Print")
            dlg.run()
            dlg.destroy()
            return
        save_file.write(text)
        save_file.close()
        cmd="./lib/pyText2pdf.py " + 'temp'
        args=shlex.split(cmd)
        process=subprocess.Popen(args,bufsize=0,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=None)
        pud=gtkunixprint.PrintUnixDialog()
        response=pud.run()
        if response==gtk.RESPONSE_OK:
            filename='temp.pdf'
            printer = pud.get_selected_printer()
            settings = pud.get_settings()
            setup = pud.get_page_setup()
            printjob = gtkunixprint.PrintJob('Printing %s' % filename, printer, settings, setup)
            printjob.set_source_file(filename)
            printjob.send(self.print_cb)
            if os.path.isfile('temp.pdf'):
                os.remove('temp.pdf')
        pud.destroy()

if __name__=="__main__":
    neuron_window=neuron()
    gtk.main()
