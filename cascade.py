#!/usr/bin/python
import gtk
import pygtk
import dbm

class cascade:
    def __init__(self):
        gladefile="./gui/cascade.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.window=builder.get_object("cascade_window")
        self.ocf_entry=builder.get_object("ocf_entry")
        self.ose_entry=builder.get_object("ose_entry")
        self.ccf_entry=builder.get_object("ccf_entry")
        self.cse_entry=builder.get_object("cse_entry")
        self.wm_entry=builder.get_object("wm_entry")
        self.cl_entry=builder.get_object("cl_entry")
        self.max_oe_entry=builder.get_object("max_oe_entry")
        self.min_oe_entry=builder.get_object("min_oe_entry")
        self.max_ce_entry=builder.get_object("max_ce_entry")
        self.min_ce_entry=builder.get_object("min_ce_entry")
        builder.connect_signals(self)

    def validate(self):
        if self.ocf_entry.get_text_length()==0:
            return False
        elif self.ose_entry.get_text_length()==0:
            return False
        elif self.ocf_entry.get_text_length()==0:
            return False
        elif self.cse_entry.get_text_length()==0:
            return False
        elif self.wm_entry.get_text_length()==0:
            return False
        elif self.cl_entry.get_text_length()==0:
            return False
        elif self.max_oe_entry.get_text_length()==0:
            return False
        elif self.min_oe_entry.get_text_length()==0:
            return False
        elif self.max_ce_entry.get_text_length()==0:
            return False
        elif self.min_ce_entry.get_text_length()==0:
            return False
        else:
            return True

    def on_ok(self,button,data=None):
        if self.validate():
            db=dbm.open('config.dat','c')
            db['Output Change Fraction']=self.ocf_entry.get_text()
            db['Output Stagnation Epochs']=self.ose_entry.get_text()
            db['Candidate Change Fraction']=self.ccf_entry.get_text()
            db['Candidate Stagnation Epochs']=self.cse_entry.get_text()
            db['Weight Multiplier']=self.wm_entry.get_text()
            db['Candidate Limit']=self.cl_entry.get_text()
            db['Maximum Out Epochs']=self.max_oe_entry.get_text()
            db['Minimum Out Epochs']=self.min_oe_entry.get_text()
            db['Maximum Candidate Epochs']=self.max_ce_entry.get_text()
            db['Minimum Candidate Epochs']=self.min_ce_entry.get_text()
            db.close()
            self.window.destroy()
        else:
            em=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_ERROR,gtk.BUTTONS_OK,"Parameters Missing")
            em.run()
            em.destroy()

    def on_cascade_window_delete_event(self,widget,data=None):
        self.window.hide()
        return True

if __name__=="__main__":
    cwindow=cascade()
    gtk.main()
