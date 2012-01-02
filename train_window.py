#!/usr/bin/python
import sys
import gtk
import pygtk
import dbm

class train_window:
    """Window For Asking Training Parameters about BPN Network"""
    def __init__(self):
        gladefile="./gui/training_window.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.train_window=builder.get_object("train_window")
        self.connrate=builder.get_object("connrate_text")
        self.lrate=builder.get_object("lrate_text")
        self.derror=builder.get_object("derror_text")
        self.miter=builder.get_object("miter_text")
        self.ireport=builder.get_object("ireport_text")
        self.function=builder.get_object("function_cb")
        self.edialog=builder.get_object("errordialog")
        builder.connect_signals(self)

    def on_ok(self,widget,data=None):
        if not self.Validate_form():
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Training Parameters Not Completed")
            em.run()
            em.destroy()
        else:
            db=dbm.open('config.dat','c')
            db['Connection Rate']=self.connrate.get_text()
            db['Learning Rate']=self.lrate.get_text()
            db['Desired Error']=self.derror.get_text()
            db['Maximum Iterations']=self.miter.get_text()
            db['Iteration Between Reports']=self.ireport.get_text()
            db['Output Layer Activation Function']=self.function.get_active_text()
            db.close()
            self.train_window.hide()

    def Validate_form(self):
        if self.connrate.get_text_length()==0:
            return False
        elif self.lrate.get_text_length()==0:
            return False
        elif self.derror.get_text_length()==0:
            return False
        elif self.miter.get_text_length()==0:
            return False
        elif self.ireport.get_text_length()==0:
            return False
        elif self.function.get_active_text()==None:
            return False
        else:
            return True
    
    def pack_param(self):
        if self.Validate_form():
            crate=self.connrate.get_text()
            lrate=self.lrate.get_text()
            derror=self.derror.get_text()
            miter=self.miter.get_text()
            ireport=self.ireport.get_text()
            ofun=self.function.get_active_text()
            tdata=[crate,lrate,derror,miter,ireport,ofun,tdata]
            return tdata
        else:
            return None


    def on_train_window_destroy(self,widget,data=None):
        self.train_window.destroy()

if __name__=="__main__":
    create_window=train_window()
    gtk.main()
