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
        self.awindow=builder.get_object("config_standard")
        
        builder.connect_signals(self)

    def on_config_standard_destroy(self,widget,data=None):
        self.awindow.destroy()

    def on_ok(self,widget,data=None):
        

if __name__=="__main__":
    create_window=askparam_window()
    gtk.main()

