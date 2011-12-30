import gtk
import pygtk

class adv_train:
    """Configure Window for Setting Advanced Parameters on Training"""
    def __init__(self):
        gladefile="adv_training.xml"
        builder=gtk.Builder()
        builder.add_from_file(gladefile)
        self.win=builder.get_object("adv_train_window")
        builder.connect_signals(self)

if __name__=="__main__":
    window=adv_train()
    window.win.show()
    gtk.main()

