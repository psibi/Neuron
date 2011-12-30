import gtk
import pygtk

class adv_train:
    """Configure Window for Setting Advanced Parameters on Training"""
    def __init__(self):
        gladefile="adv_training.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.win=builder.get_object("adv_train_window")
        self.vbox4=builder.get_object("vbox4")
        self.vbox5=builder.get_object("vbox5")
        self.vbox6=builder.get_object("vbox6")
        self.vbox7=builder.get_object("vbox7")
        self.vbox8=builder.get_object("vbox8")
        self.vbox10=builder.get_object("vbox10")
        self.af_liststore=builder.get_object("af_liststore")
        builder.connect_signals(self)
        
    def show(self):
        self.win.show()

    def on_add_afn(self,button,data=None):
        entry=gtk.Entry()
        cb = gtk.ComboBox(self.af_liststore)
        cell=gtk.CellRendererText()
        cb.pack_start(cell,True)
        cb.add_attribute(cell,'text',0)
        self.vbox5.pack_start(cb, True, True, 1)
        self.vbox4.pack_start(entry,True,True,1)
        cb.show()
        entry.show()


    def on_add_afl(self,button,data=None):
        entry=gtk.Entry()
        cb = gtk.ComboBox(self.af_liststore)
        cell=gtk.CellRendererText()
        cb.pack_start(cell,True)
        cb.add_attribute(cell,'text',0)
        self.vbox7.pack_start(cb, True, True, 1)
        self.vbox6.pack_start(entry,True,True,1)
        cb.show()
        entry.show()        

    def on_add_asn(self,button,data=None):
        entry=gtk.Entry()
        self.vbox8.pack_start(entry,True,True,1)
        entry.show()

    def on_add_asl(self,button,data=None):
        entry=gtk.Entry()
        self.vbox10.pack_start(entry,True,True,1)
        entry.show()

    def on_ok(self,button,data=None):
        self.win.destroy()

    def on_cancel(self,button,data=None):
        self.win.destroy()

if __name__=="__main__":
    window=adv_train()
    window.win.show()
    gtk.main()

