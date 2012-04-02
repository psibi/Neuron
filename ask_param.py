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
import sys
import gtk
import pygtk
import dbm
from train_window import train_window

class askparam_window:
    """Window For Asking Parameters about BPN Network"""
    def __init__(self,net):
        gladefile="./gui/config_parameter.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.type=net
        self.awindow=builder.get_object("config_standard")
        self.clabel=builder.get_object("config_label")
        self.numl_text=builder.get_object("numl_text")
        self.inputn_text=builder.get_object("inputn_text")
        self.outputn_text=builder.get_object("outputn_text")
        self.hiddenn_text=builder.get_object("hiddenn_text")
        self.numh_text=builder.get_object("numh_text")
        if (net == "SPR"):
            self.clabel.set_label("Enter Sparse BPN Parameters")
        elif (net == "STD"):
            self.clabel.set_label("Enter Standard BPN Parameters")
        elif (net == "SRT"):
            self.clabel.set_label("Enter Shortcut BPN Parameters")
        builder.connect_signals(self)

    def on_config_standard_destroy(self,widget,data=None):
        """Handler for the destroy event for the window."""
        self.awindow.destroy()

    def on_ok(self,widget,data=None):
        """Handler for the OK button for the window which is raised
        whenever it is clicked"""
        if not self.validate_parameters():
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Incorrect Parameters")
            em.run()
            em.destroy()
        else:
            db=dbm.open('config.dat','c')
            db['Network Type']=self.type
            db['Number of Layers']=self.numl_text.get_text()
            db['Input Neurons']=self.inputn_text.get_text()
            db['Output Neurons']=self.outputn_text.get_text()
            db['Hidden Neurons']=self.hiddenn_text.get_text()
            db['Number of Hidden Layers']=self.numh_text.get_text()
            db.close()
            self.awindow.hide()
            try:
                db=dbm.open('config.dat','c')
                temp=db['Maximum Neurons']
                db.close()
            except KeyError:
                twindow=train_window()

    def validate_parameters(self):
        """For Validating the Entry present in the Ask Parameter Window"""
        if self.numl_text.get_text_length()==0:
            return False
        elif self.inputn_text.get_text_length()==0:
            return False
        elif self.outputn_text.get_text_length()==0:
            return False
        elif self.hiddenn_text.get_text_length()==0:
            return False
        elif self.numh_text.get_text_length()==0:
            return False
        elif int(self.numl_text.get_text())-int(self.numh_text.get_text())!=2:
            return False
        elif int(self.numh_text.get_text())>1:
            numh_layers = int(self.numh_text.get_text())
            hidden_neurons = self.hiddenn_text.get_text()
            no_commas = len(hidden_neurons.split(",")) #Returns total commas + 1
            if no_commas!=numh_layers:
                return False
            else:
                return True
        else:
            return True

if __name__=="__main__":
    create_window=askparam_window("SPR")
    gtk.main()

