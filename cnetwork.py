#!/usr/bin/python
import gtk
import pygtk

class cnetwork:
    """Window for configuring Network Type"""
    def __init__(self):
        gladefile="./gui/network_conf.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("network_conf")
        builder.connect_signals(self)

    def on_ok(self,button,data=None):
        self.window.destroy()

    def on_cancel(self,button,data=None):
        self.window.destroy()
        
    def show(self):
        self.window.show()

if __name__=="__main__":
    cwindow=cnetwork()
    cwindow.window.show()
    gtk.main()

