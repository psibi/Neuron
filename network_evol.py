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
import gtk
import pygtk
import dbm

class Network_evol:
    """Window for Evolving topology Network."""
    def __init__(self):
        gladefile="./gui/network_evol.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("evol_window")
        self.maxn_entry=builder.get_object("maxn_entry")
        self.nbr_entry=builder.get_object("nbr_entry")
        self.de_entry=builder.get_object("de_entry")
        builder.connect_signals(self)
    
    def show(self):
        """For displaying the window."""
        self.window.show()

    def on_ok(self,button,data=None):
        """Handler for OK button on the window when it is clicked."""
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Maximum Neurons']=self.maxn_entry.get_text()
            db['Neurons Between Reports']=self.nbr_entry.get_text()
            db['Desired Error']=self.de_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        """Handler for the Cancel button on the window when it is clicked."""
        self.window.destroy()

    def validate(self):
        """For validating the Entry present in the window."""
        if self.maxn_entry.get_text_length()==0:
            return False
        elif self.nbr_entry.get_text_length()==0:
            return False
        elif self.de_entry.get_text_length()==0:
            return False
        else:
            return True
        
    def on_evol_window_delete_event(self,widget,data=None):
        """Handler for the delete event in the window."""
        self.window.destroy()
        return True

if __name__=="__main__":
    nwindow=Network_evol()
    nwindow.window.show()
    gtk.main()


