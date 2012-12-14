#!/usr/bin/env python

DEBUG = False

import cairo
#from gi.repository import Gtk, Gdk
from gi.repository import Unity, GObject, Gtk, Notify, Gdk
import os

try:
    import actmon
except ImportError:
    class FakeActmon():
        def get_idle_time(self):
            return 0
    actmon = FakeActmon()

#TODO
# HIGH IMPORTANCE
# Window uncloseable
#
# LOW IMPORTANCE
# create timer class
# Add tray icon
# Add appindicator
# Add unity indicator

class StatusIcon(Gtk.StatusIcon):
    def __init__(self):
        super(StatusIcon, self).__init__()
        self.set_tooltip_text("Take a break")
        self.set_from_stock(Gtk.STOCK_CANCEL)
        self.set_visible(True)

        self.connect('activate', self.icon_click)
        self.connect('popup-menu', self.menu_open)

    def icon_click(self, data):
        print "tray icon clicked", data
#        main_window.start_break()

    def menu_open(self, icon, button, time):
        main_window.tray_menu.show_all()
        def pos(menu, icon):
            return Gtk.StatusIcon.position_menu(menu, icon)
        main_window.tray_menu.popup(None, None, pos, self, button, time)


class FullScreenWindow(Gtk.Window):
    if DEBUG:
        work_time = 10
        break_time = 6
        long_break = 5
        postpone_time = 2
        idle_time = 5
    else:
        work_time = 45*60
        break_time = 5*60
        long_break = 10*60
        postpone_time = 3*60
        idle_time = 1*60

    text_style = '<span foreground="white" font="36">%text%</span>'

    def __init__(self):
        # main_window properties
        super(FullScreenWindow, self).__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
#        self.set_border_width(30)
        self.fullscreen()
        self.set_keep_above(True)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            print "[INFO] Compositing enabled"
            self.set_visual(self.visual)
        self.set_app_paintable(True)

        # main_box
        self.tray_menu = builder.get_object('tray_menu')

        main_box = builder.get_object('main_box')
        self.time_lbl = builder.get_object('time_lbl')
        self.time_lbl.set_property("use-markup", True)

        self.time_lbl = builder.get_object('time_lbl')
        self.time_lbl.set_property("use-markup", True)

        handlers = {
            "postpone": self.postpone,
            "skip": self.skip,
            "menu_break": self.take_break,
            "menu_quit": Gtk.main_quit,
        }
        builder.connect_signals(handlers)

        main_box.reparent(self)
        self.add(main_box)

        # main_window events
        self.connect("draw", self.redraw)
        self.connect("delete-event", Gtk.main_quit)
        # TODO uncomment to make uncloseable
#        self.connect("delete-event", lambda widget, event: True)
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
        GObject.timeout_add_seconds(1, self.tick)
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
            time = str( self.format_time(self.counter) )
            if self.time == "break":
                self.time_lbl.set_label( self.text_style.replace("%text%", time) )
            else:
                status_icon.set_tooltip_text("Next break in %s" % (time))
                builder.get_object('time_remaining').set_label(time)
            if actmon.get_idle_time() > self.idle_time*1000 and self.time == "work":
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
        
    def take_break(self, widget):
        self.start_break()


if __name__ == "__main__":
#    screen = Gdk.Screen.get_default()
#    css_provider = Gtk.CssProvider()
#    css_provider.load_from_path('metro.css')
#    
#    context = Gtk.StyleContext()
#    context.add_provider_for_screen(screen, css_provider,
#                                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    builder = Gtk.Builder()
    pth = os.path.dirname(os.path.realpath(__file__))
    builder.add_from_file(pth + "/good.glade")
    #builder.add_objects_from_file(pth + "/good.glade", ('main_box', 'time_lbl', 'tray_menu', ''))

    status_icon = StatusIcon()
    main_window = FullScreenWindow()
    Gtk.main()

