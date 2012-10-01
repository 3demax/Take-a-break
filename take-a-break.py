#!/usr/bin/env python

import cairo
from gi.repository import Gtk, Gdk

class FullScreenWindow(Gtk.Window):
    def __init__(self):
    
        builder = Gtk.Builder()
        builder.add_from_file("good.glade")

        super(FullScreenWindow, self).__init__()
        main_box = builder.add_objects_from_file("good.glade", ('main_box'))
        main_box = builder.get_object('main_box')
        
        handlers = {
            "postpone": self.postpone,
            "skip": self.skip
        }
        builder.connect_signals(handlers)

        main_box.reparent(self)
        self.add(main_box)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(30)
        self.fullscreen()
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            print "[INFO] Compositing on"
            self.set_visual(self.visual)

        self.set_app_paintable(True)
        self.connect("draw", self.redraw)
        self.connect("delete-event", Gtk.main_quit)
        self.connect('key-press-event', self.draw_something)
        

        
        self.show_all()

    def redraw(self, widget, cr):
        self.cr = cr
#        print cr, self.cr
        self.cr.set_source_rgba(.1, .1, .1, 0.9)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.cr.paint()
        self.cr.set_operator(cairo.OPERATOR_OVER)
    
    def draw_something(self, widget, cr):
        print ("\ndraw something")
        cr = self.cr
        self.queue_draw()
#        print cr
        cr.set_source_rgba(1.0, .0, .0, 1.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def postpone(self, widget):
        print "postpone"
#        self.hide()
        pass

    def skip(self, widget):
        print "skip"
#        self.hide()
        pass

if __name__ == "__main__":
    main_window = FullScreenWindow()
    Gtk.main()

