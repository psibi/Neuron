#!/usr/bin/python
import gtk
import pygtk
import dbm

class qprop:
    def __init__(self):
        gladefile="./gui/qprop.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("qprop_window")
        self.decay_entry=builder.get_object("decay_entry")
        self.mu_entry=builder.get_object("mu_entry")
        builder.connect_signals(self)

    def on_ok(self,button,data=None):
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Decay Value']=self.decay_entry.get_text()
            db['Mu Value']=self.mu_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        self.window.destroy()

    def validate(self):
        if self.decay_entry.get_text_length()==0:
            return False
        elif self.mu_entry.get_text_length()==0:
            return False
        else:
            return True

    def on_qprop_window_delete_event(self,widget,data=None):
        self.window.destroy()
        return True

if __name__=="__main__":
    qprop_w=qprop()
    gtk.main()
