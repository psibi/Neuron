#!/usr/bin/python
import gtk
import pygtk
from network_evol import Network_evol

class cnetwork:
    """Window for configuring Network Type"""
    def __init__(self):
        gladefile="./gui/network_conf.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("network_conf")
        self.fixed_rb=builder.get_object("fixed_rb")
        self.evolving_rb=builder.get_object("evolving_rb")
        builder.connect_signals(self)

    def on_ok(self,button,data=None):
        """Handler for the OK button present in the cnetwork window."""
        if self.evolving_rb.get_active():
            self.window.hide()
            nwindow=Network_evol()
            nwindow.show()
        else:
            self.window.hide()

    def on_cancel(self,button,data=None):
        """Handler for the Cancel button present in the cnetwork."""
        self.window.hide()
        
    def show(self):
        """For showing the Configure Network Type(cnetwork) window."""
        self.window.show()

    def on_evolving_rb_toggled(self,radiobutton,data=None):
        pass

    def on_network_conf_delete_event(self,widget,data=None):
        """Delete event handler for the cnetwork window."""
        self.window.hide()

if __name__=="__main__":
    cwindow=cnetwork()
    cwindow.window.show()
    gtk.main()

