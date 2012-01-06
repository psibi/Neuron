#!/usr/bin/python
import gtk
import pygtk
import dbm

class rprop:
    def __init__(self):
        gladefile="./gui/rprop.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("rprop_window")
        self.if_entry=builder.get_object("if_entry")
        self.df_entry=builder.get_object("df_entry")
        self.dmin_entry=builder.get_object("dmin_entry")
        self.dmax_entry=builder.get_object("dmax_entry")
        self.dzero_entry=builder.get_object("dzero_entry")
        builder.connect_signals(self)

    def on_ok(self,button,data=None):
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Increase Factor']=self.if_entry.get_text()
            db['Decrease Factor']=self.df_entry.get_text()
            db['Delta Minimum']=self.dmin_entry.get_text()
            db['Delta Maximum']=self.dmax_entry.get_text()
            db['Delta Zero']=self.dzero_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cancel(self,button,data=None):
        self.window.destroy()

    def validate(self):
        if self.if_entry.get_text_length()==0:
            return False
        elif self.df_entry.get_text_length()==0:
            return False
        elif self.dmin_entry.get_text_length()==0:
            return False
        elif self.dmax_entry.get_text_length()==0:
            return False
        elif self.dzero_entry.get_text_length()==0:
            return False
        else:
            return True

    def on_rprop_window_delete_event(self,widget,data=None):
        self.window.destroy()
        return True

if __name__=="__main__":
    rprop_w=rprop()
    gtk.main()
