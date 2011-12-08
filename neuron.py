import sys
import gtk
import pygtk

#!/usr/bin/python
class neuron:
    """Main Neuron Application"""
    def __init__(self):
        gladefile="neural.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("mainwindow")
        builder.connect_signals(self)

    def on_mainwindow_destroy(self,widget,data=None):
        gtk.main_quit()

    def on__Quit_activate(self,widget,data=None):
        gtk.main_quit()

if __name__=="__main__":
    neuron_window=neuron()
    gtk.main()


        
