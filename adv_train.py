import gtk
import pygtk
import dbm

class adv_train:
    """Configure Window for Setting Advanced Parameters on Training"""
    def __init__(self):
        gladefile="./gui/adv_training.xml"
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
        self.afn_combobox=builder.get_object("afn_combobox")
        self.afl_combobox=builder.get_object("afl_combobox")
        self.lmomentum=builder.get_object("lmomentum")
        self.af_neuron=builder.get_object("af_neuron")
        self.af_layer=builder.get_object("af_layer")
        self.as_neuron=builder.get_object("as_neuron")
        self.as_layer=builder.get_object("as_layer")
        self.tef_combobox=builder.get_object("tef_combobox")
        self.tsf_combobox=builder.get_object("tsf_combobox")
        self.bflimit=builder.get_object("bflimit")
        builder.connect_signals(self)
        
    def show(self):
        """For displaying the Advanced Training Window."""
        self.win.show()

    def validate(self):
        """For Validating the GTK Enty widgets present in the window."""
        if self.lmomentum.get_text_length()==0:
            return False
        elif self.af_neuron.get_text_length()==0:
            return False
        elif self.af_layer.get_text_length()==0:
            return False
        elif self.as_neuron.get_text_length()==0:
            return False
        elif self.as_layer.get_text_length()==0:
            return False
        elif self.bflimit.get_text_length()==0:
            return False
        else:
            return True

    def on_add_afn(self,button,data=None):
        """For dynamically adding Entry Box and Comboxbox
        related to Activation Function of a neuron on clicking the + button."""
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
        """For dynamically adding Entry box and Combobox related to Activation
        Function of a layer on clicking the + button."""
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
        """For dynamically adding Entry box for Activation Steepness for
        a neuron."""
        entry=gtk.Entry()
        self.vbox8.pack_start(entry,True,True,1)
        entry.show()

    def on_add_asl(self,button,data=None):
        """For dynamically adding Entry box for Activation Steepness for
        a layer."""
        entry=gtk.Entry()
        self.vbox10.pack_start(entry,True,True,1)
        entry.show()

    def on_ok(self,button,data=None):
        """Handler for the OK button in the Advanced Training Window."""
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Learning Momentum']=self.lmomentum.get_text()
            db['AF for Neuron']=self.af_neuron.get_text()
            db['AF Neuron']=self.afn_combobox.get_active_text()
            db['AF for layer']=self.af_layer.get_text()
            db['AF Layer']=self.afl_combobox.get_active_text()
            db['Activation Steepness for Neuron']=self.as_neuron.get_text()
            db['Activation Steepness for layer']=self.as_layer.get_text()
            db['Train Error Function']=self.tef_combobox.get_active_text()
            db['Train Stop Function']=self.tsf_combobox.get_active_text()
            db['Bit Fail Limit']=self.bflimit.get_text()
            db.close()
            self.win.destroy()            
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Not Completed")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        """Handler for the Cancel button in the Advanced Training Window."""
        self.win.destroy()

    
if __name__=="__main__":
    window=adv_train()
    window.win.show()
    gtk.main()

