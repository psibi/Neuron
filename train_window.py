#!/usr/bin/python
import sys
import gtk
import pygtk

class train_window:
    """Window For Asking Training Parameters about BPN Network"""
    def __init__(self):
        gladefile="training_window.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        builder.connect_signals(self)
        
if __name__=="__main__":
    create_window=train_window()
    gtk.main()
