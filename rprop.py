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

class rprop:
    """Window for displaying parameters related to RPROP algorithm."""
    def __init__(self):
        gladefile="./gui/rprop.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("rprop_window")
        self.if_entry=builder.get_object("if_entry")
        self.df_entry=builder.get_object("df_entry")
        self.dmin_entry=builder.get_object("dmin_entry")
        self.dmax_entry=builder.get_object("dmax_entry")
        self.dzero_entry=builder.get_object("dzero_entry")
        builder.connect_signals(self)

    def on_ok(self,button,data=None):
        """Handler for the OK button which is invoked when it is clicked."""
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Increase Factor']=self.if_entry.get_text()
            db['Decrease Factor']=self.df_entry.get_text()
            db['Delta Minimum']=self.dmin_entry.get_text()
            db['Delta Maximum']=self.dmax_entry.get_text()
            db['Delta Zero']=self.dzero_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        """Handler for the cancel button which is invoked when it is clicked."""
        self.window.destroy()

    def validate(self):
        """For validating the Entry present in the window."""
        if self.if_entry.get_text_length()==0:
            return False
        elif self.df_entry.get_text_length()==0:
            return False
        elif self.dmin_entry.get_text_length()==0:
            return False
        elif self.dmax_entry.get_text_length()==0:
            return False
        elif self.dzero_entry.get_text_length()==0:
            return False
        else:
            return True

    def on_rprop_window_delete_event(self,widget,data=None):
        """Delete event handler in the window."""
        self.window.destroy()
        return True

if __name__=="__main__":
    rprop_w=rprop()
    gtk.main()
