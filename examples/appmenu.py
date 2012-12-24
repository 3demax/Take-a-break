#!/usr/bin/env python
#
# Copyright 2009-2012 Canonical Ltd.
#
# Authors: Neil Jagdish Patel <neil.patel@canonical.com>
#          Jono Bacon <jono@ubuntu.com>
#          David Planella <david.planella@ubuntu.com>
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of either or both of the following licenses:
#
# 1) the GNU Lesser General Public License version 3, as published by the 
# Free Software Foundation; and/or
# 2) the GNU Lesser General Public License version 2.1, as published by 
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the applicable version of the GNU Lesser General Public 
# License for more details.
#
# You should have received a copy of both the GNU Lesser General Public 
# License version 3 and version 2.1 along with this program.  If not, see 
# <http://www.gnu.org/licenses/>
#

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


def menuitem_response(w, buf):
  print buf

if __name__ == "__main__":
  ind = appindicator.Indicator.new (
                        "example-simple-client",
                        "indicator-messages",
                        appindicator.IndicatorCategory.APPLICATION_STATUS)
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)
  ind.set_attention_icon ("indicator-messages-new")

  # create a menu
  menu = Gtk.Menu()

  # create some 
  for i in range(3):
    buf = "Test-undermenu - %d" % i

    menu_items = Gtk.MenuItem(buf)

    menu.append(menu_items)

    # this is where you would connect your menu item up with a function:
    
    menu_items.connect("activate", menuitem_response, buf)

    # show the items
    menu_items.show()

  #quit
  menu_items = Gtk.MenuItem("quit")
  menu.append(menu_items)
  # this is where you would connect your menu item up with a function:
  menu_items.connect("activate", Gtk.main_quit)
  # show the items
  menu_items.show()


  ind.set_menu(menu)

  Gtk.main()

