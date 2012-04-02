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
from ask_param import askparam_window

class selectbpn_window:
    """Window For Selecting BPN Network"""
    def __init__(self):
        gladefile="./gui/n_create.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("create_window")
        self.standard=builder.get_object("standard_rb")
        self.sparse=builder.get_object("sparse_rb")
        self.shortcut=builder.get_object("shortcut_rb")
        self.network=[]
        builder.connect_signals(self)
        self.standard.toggled()

    def on_create_window_destroy(self,widget,data=None):
        """Destroy Event handler in the window."""
        self.window.destroy()

    def on_network_selection(self,radiomenuitem,data=None):
        """This method invoked whenever the radiobutton emits a toggled signal."""
        if self.standard.get_active():
            del self.network[:]
            self.network.append("STD")
        elif self.sparse.get_active():
            del self.network[:]
            self.network.append("SPR")
        elif self.shortcut.get_active():
            del self.network[:]
            self.network.append("SRT")

    def get_network(self):
        """Return the BPN network selected."""
        return self.network

    def on_next(self,widget,data=None):
        """Handler invoked on clicking the Next button."""
        db=dbm.open('config.dat','c')
        db['network']=self.network[0]
        db.close()
        self.window.hide()
        askwin=askparam_window(self.network[0])

if __name__=="__main__":
    create_window=selectbpn_window()
    gtk.main()

