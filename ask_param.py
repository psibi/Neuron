#!/usr/bin/python
import sys
import gtk
import pygtk

class askparam_window:
    """Window For Asking Parameters about BPN Network"""
    def __init__(self):
        gladefile="config_parameter.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
       
        builder.connect_signals(self)

    def on_config_standard_destroy(self,widget,data=None):
        gtk.main_quit()

    def get_network(self):
        return self.network

if __name__=="__main__":
    create_window=askparam_window()
    gtk.main()

