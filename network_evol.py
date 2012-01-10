#!/usr/bin/python
import gtk
import pygtk
import dbm

class Network_evol:
    def __init__(self):
        gladefile="./gui/network_evol.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("evol_window")
        self.maxn_entry=builder.get_object("maxn_entry")
        self.nbr_entry=builder.get_object("nbr_entry")
        self.de_entry=builder.get_object("de_entry")
        builder.connect_signals(self)
    
    def show(self):
        self.window.show()

    def on_ok(self,button,data=None):
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Maximum Neurons']=self.maxn_entry.get_text()
            db['Neurons Between Reports']=self.nbr_entry.get_text()
            db['Desired Error']=self.de_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        self.window.destroy()

    def validate(self):
        if self.maxn_entry.get_text_length()==0:
            return False
        elif self.nbr_entry.get_text_length()==0:
            return False
        elif self.de_entry.get_text_length()==0:
            return False
        else:
            return True
        
    def on_evol_window_delete_event(self,widget,data=None):
        self.window.destroy()
        return True

if __name__=="__main__":
    nwindow=Network_evol()
    nwindow.window.show()
    gtk.main()


