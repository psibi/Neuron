#!/usr/bin/python
import sys
import gtk
import pygtk

class selectbpn_window:
    """Window For Selecting BPN Network"""
    def __init__(self):
        gladefile="n_create.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("create_window")
        self.standard=builder.get_object("standard_rb")
        self.sparse=builder.get_object("sparse_rb")
        self.shortcut=builder.get_object("shortcut_rb")
        self.network=[]
        builder.connect_signals(self)

    def on_create_window_destroy(self,widget,data=None):
        self.window.destroy()

    def on_network_selection(self,radiomenuitem,data=None):
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
        return self.network

if __name__=="__main__":
    create_window=selectbpn_window()
    gtk.main()

