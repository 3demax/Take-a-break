#!/usr/bin/env python

import cairo
from gi.repository import Gtk, Gdk
from gi.repository import Unity, GObject, Gtk, Notify, Gdk, Pango, GLib

try:
    import actmon
except:
    actmon = object()
    actmon.get_idle_time = lambda x: 0

#TODO
# HIGH IMPORTANCE
# Window on top
# Window uncloseable
#
# LOW IMPORTANCE
# create timer class
# Add tray icon
# Add appindicator
# Add unity indicator

class FullScreenWindow(Gtk.Window):
    work_time = 45*60
    break_time = 5*60
    long_break = 10*60
    postpone_time = 1*60
    idle_time = 1*60
    
    text_style = '<span foreground="white" font="36">%text%</span>'
    
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("good.glade")

        super(FullScreenWindow, self).__init__()
        builder.add_objects_from_file("good.glade", ('main_box', 'time_lbl'))
        main_box = builder.get_object('main_box')
        self.time_lbl = builder.get_object('time_lbl')
#        self.time_lbl.use_markup(True)
        
        handlers = {
            "postpone": self.postpone,
            "skip": self.skip
        }
        builder.connect_signals(handlers)

        main_box.reparent(self)
        self.add(main_box)
        self.time_lbl.set_property("use-markup", True)

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
        
        self.timer_boot()

    # ================
    # event callbacks
    # ================

    def redraw(self, widget, cr):
        self.cr = cr
        self.cr.set_source_rgba(.1, .1, .1, 0.9)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.cr.paint()
        self.cr.set_operator(cairo.OPERATOR_OVER)
    
    def draw_something(self, widget, cr):
        print ("\ndraw something")
        cr = self.cr
        self.queue_draw()
        cr.set_source_rgba(1.0, .0, .0, 1.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def format_time(self, interval):
        return "%d:%.2d" % (interval/60, interval%60)

    # timer functions
    # TODO create timer class
    def timer_boot(self):
        # TODO is this the most efficient and power-saving timer?
        GObject.timeout_add(1000, self.tick)
        self.timer_play()
        self.start_work()
    
    def start_work(self, timeout=None):
        if timeout is None:
            timeout = self.work_time
        self.time = "work"
        self.hide()
        self.set_timer(timeout)
    
    def start_break(self, timeout=None):
        if timeout is None:
            timeout = self.break_time
        self.time = "break"
        self.show()
        #TODO make long break after 3 short ones
        self.set_timer(timeout)

    def timer_pause(self):
        self.timer_counting = False
    
    def timer_play(self):
        self.timer_counting = True

    def tick(self):
        if self.counter > 0:
            if self.time == "break":
                time = str( self.format_time(self.counter) )
                self.time_lbl.set_label( self.text_style.replace("%text%", time) )
            if actmon.get_idle_time() > self.idle_time*1000:
                self.timer_pause()
            else:
                self.timer_play()
            if self.timer_counting:
                self.counter -= 1
        else:
            if self.time == "break":
                self.start_work()
            else:
                self.start_break()
        return True

    def set_timer(self, timeout=2):
        print "timeout in", timeout
        self.counter = timeout

    # button callbacks
    def postpone(self, widget):
        self.start_work(self.postpone_time)

    def skip(self, widget):
        #TODO prevent ocassinally skipping with "are you sure?" dialog
        self.start_work()


if __name__ == "__main__":
    main_window = FullScreenWindow()
    Gtk.main()

