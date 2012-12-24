from gi.repository import Gtk, cairo, GdkPixbuf

def draw_background():
    surface = cairo.ImageSurface.create_from_png('gwget.png')
    #sp = cairo.SurfacePattern(surface)
    #sp.set_extend(cairo.EXTEND_REPEAT)
    #context.set_source(sp)
    #context.paint()
    return surface

class aStatusIcon:
    def __init__(self):
        self.statusicon = Gtk.StatusIcon()
        #self.statusicon.set_from_stock(Gtk.STOCK_HOME)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('icons/white/135.svg', 48, 48)
        self.statusicon.set_from_pixbuf(pixbuf);
        self.statusicon.connect("popup-menu", self.right_click_event)
        #self.statusicon.connect("draw", draw_background)


        window = Gtk.Window()
        window.connect("destroy", lambda w: Gtk.main_quit())
        window.show_all()

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()

        about = Gtk.MenuItem()
        about.set_label("About")
        quit = Gtk.MenuItem()
        quit.set_label("Quit")

        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", Gtk.main_quit)

        self.menu.append(about)
        self.menu.append(quit)

        self.menu.show_all()

        def pos(menu, icon):
            return (Gtk.StatusIcon.position_menu(menu, icon))

        self.menu.popup(None, None, pos, self.statusicon, button, time)

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("StatusIcon Example")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Andrew Steele"])

        about_dialog.run()
        about_dialog.destroy()

aStatusIcon()
Gtk.main()


