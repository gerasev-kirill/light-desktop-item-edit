# -*- coding: utf-8 -*-
#   Simple desktop item edit
#   Copyright (C) 2012  Gerasev Kirill
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Library General Public
#   License as published by the Free Software Foundation; either
#   version 2 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import gettext
import locale
from gi.repository import Gtk, Gdk, GdkPixbuf
from ini import Ini


class MainWindow(object):

    def __init__(self, data_dir, desktop_file_path, pkgname):
        self.file_path = data_dir
        self.dfile = Ini(desktop_file_path)
        self.user_set_img = False

        gettext.bindtextdomain(pkgname, os.path.dirname(data_dir) + "/locale")
        gettext.textdomain(pkgname)
        locale.bind_textdomain_codeset(pkgname, 'UTF-8')
        _ = gettext.gettext
        self._ = _

        self.tree = Gtk.Builder()
        self.tree.set_translation_domain(
            "light-desktop-item-edit")  # doesn't work at all
        self.tree.add_from_file(
            os.path.join(self.file_path, 'desktop-item-edit.ui'))
        for obj in self.tree.get_objects():
            if obj.__gtype__ == Gtk.Label.__gtype__ or obj.__gtype__ == Gtk.CheckButton.__gtype__:
                obj.set_label(_(obj.get_label()))

        self.tree.get_object("browse").set_label(_("Browse..."))
        self.tree.get_object("dialog").set_title(_("Launcher"))

        list_store = Gtk.ListStore(str)
        self.positions = [_('Application'),
                          _('Application in terminal'),
                          _('Location')]
        for pos in self.positions:
            list_store.append([pos])
        self.combobox = Gtk.ComboBox.new_with_model(list_store)
        renderer_text = Gtk.CellRendererText()
        self.combobox.pack_start(renderer_text, True)
        self.combobox.add_attribute(renderer_text, "text", 0)
        self.combobox.set_active(0)

        combobox_container = self.tree.get_object("combobox-container")
        combobox_container.pack_start(self.combobox, False, False, True)

        self.img = Gtk.Image()
        self.tree.get_object("icon-button").add(self.img)

        self.load_desktop_file()

        self.combobox.connect("changed", self.combobox_changed)
        self.tree.get_object("ok").connect("clicked", self.ok_pressed)
        self.tree.get_object("cancel").connect("clicked", self.destroy)
        self.tree.get_object("command").connect(
            "changed", self.command_changed)
        self.tree.get_object("name").connect("changed", self.name_changed)
        self.tree.get_object("browse").connect("clicked", self.browse_pressed)
        self.tree.get_object("icon-button").connect(
            "clicked", self.icon_pressed)

        w = self.tree.get_object("dialog")
        w.connect("key-press-event", self.handle_escape)
        w.show_all()
        Gtk.main()

    def handle_escape(self, w, e):
        if e.keyval == Gdk.KEY_Escape:
            self.destroy(0)

    def combobox_changed(self, n):
        if self.combobox.get_active() == 2:
            self.tree.get_object("label-lc").set_label(self._("Location:"))
        else:
            self.tree.get_object("label-lc").set_label(self._("Command:"))

    def name_changed(self, w):
        text = self.tree.get_object("name").get_text()
        if text.__len__() == 0:
            self.tree.get_object("ok").set_sensitive(False)
        else:
            self.tree.get_object("ok").set_sensitive(True)

    def command_changed(self, w):
        text = self.tree.get_object("command").get_text()
        self.dfile.set("Icon", text.split(" ")[0])
        if text.split(" ")[0].__len__() == 0:
            self.user_set_img = False
            self.tree.get_object("ok").set_sensitive(False)
        else:
            self.tree.get_object("ok").set_sensitive(True)
        self.load_icon()

    def icon_pressed(self, n):
        fc_dialog = Gtk.FileChooserDialog()
        filter = Gtk.FileFilter()
        filter.set_name(self._("Images"))
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        fc_dialog.add_filter(filter)

        if os.path.isfile(self.dfile.get("Icon")):
            fc_dialog.set_filename(self.dfile.get("Icon"))
        else:
            fc_dialog.set_current_folder(os.path.expanduser("~"))

        fc_dialog.set_title(self._("Choose an icon..."))
        fc_dialog.set_action(Gtk.FileChooserAction.OPEN)
        fc_dialog.set_default_response(Gtk.ResponseType.OK)
        fc_dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)  # ,
        fc_dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = fc_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dfile.set("Icon", fc_dialog.get_filename())
            self.user_set_img = False
            self.load_icon()
        fc_dialog.destroy()

    def browse_pressed(self, n):
        fc_dialog = Gtk.FileChooserDialog()
        if self.combobox.get_active() == 2:
            fc_dialog.set_current_folder(os.path.expanduser("~"))
            fc_dialog.set_title(self._("Choose location..."))
            fc_dialog.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        else:
            fc_dialog.set_current_folder(os.path.expanduser("~"))
            fc_dialog.set_title(self._("Choose an application..."))
            fc_dialog.set_action(Gtk.FileChooserAction.OPEN)

        fc_dialog.set_default_response(Gtk.ResponseType.OK)
        fc_dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)  # ,
        fc_dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = fc_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.tree.get_object("command").set_text(fc_dialog.get_filename())
        fc_dialog.destroy()

    def load_icon(self):
        if self.dfile.get("Icon").__contains__("/") and not self.user_set_img:
            image = Gtk.Image()
            image.set_from_file(self.dfile.get("Icon"))
            pixbuf = image.get_pixbuf()
            if not pixbuf:
                icon = Gtk.IconTheme.get_default()
                pixbuf = icon.load_icon("gtk-missing-image", 48, 0)
                self.img.set_from_pixbuf(pixbuf)
                return
            if pixbuf.get_width() > 100:
                x = (100.0 * pixbuf.get_height()) / pixbuf.get_width()
                y = 100
                pixbuf = pixbuf.scale_simple(
                    y, int(x), GdkPixbuf.InterpType.BILINEAR)

            self.img.set_from_pixbuf(pixbuf)

            self.user_set_img = True
        else:
            self.load_default_icon()
            icon = Gtk.IconTheme.get_default()
            try:
                pixbuf = icon.load_icon(self.dfile.get("Icon"), 48, 0)
                self.img.set_from_pixbuf(pixbuf)
                self.user_set_img = True
            except:
                if not self.user_set_img:
                    pixbuf = icon.load_icon("gtk-missing-image", 48, 0)
                    self.img.set_from_pixbuf(pixbuf)

    def load_desktop_file(self):
        self.tree.get_object("name").set_text(self.dfile.get("Name"))
        self.tree.get_object("command").set_text(self.dfile.get("Exec"))
        self.tree.get_object("categories").set_text(
            self.dfile.get("Categories"))
        self.tree.get_object("comment").set_text(self.dfile.get("Comment"))
        self.tree.get_object("showonlyin").set_text(
            self.dfile.get("ShowOnlyIn"))

        if self.dfile.get("StartupNotify") == "true":
            self.tree.get_object("checkbutton-sturtup").set_active(True)
        else:
            self.tree.get_object("checkbutton-sturtup").set_active(False)

        self.load_icon()

        if self.dfile.get("Terminal") == "true":
            self.combobox.set_active(1)
        else:
            self.combobox.set_active(0)
        if self.dfile.get("Type") == "Link":
            self.combobox.set_active(2)

    def save_desktop_file(self):
        name = self.tree.get_object("name").get_text()
        command = self.tree.get_object("command").get_text()
        categories = self.tree.get_object("categories").get_text()
        comment = self.tree.get_object("comment").get_text()
        showonlyin = self.tree.get_object("showonlyin").get_text()

        if os.environ.has_key("LANG"):
            LANG = os.environ["LANG"][:5]
            LANG = "[" + LANG + "]"
        else:
            LANG = ""

        self.dfile.set("Name" + LANG, name)
        self.dfile.set("Name", name)

        if self.combobox.get_active() == 0:
            self.dfile.set("Exec", command)
            self.dfile.set("Terminal", "false")
            self.dfile.set("Type", "Application")
        elif self.combobox.get_active() == 1:
            self.dfile.set("Exec", command)
            self.dfile.set("Terminal", "true")
            self.dfile.set("Type", "Application")
        elif self.combobox.get_active() == 2:
            self.dfile.set("URL", command)
            self.dfile.set("Type", "Link")
            self.dfile.remove("Exec")
            self.dfile.remove("Terminal")

        if self.tree.get_object("checkbutton-sturtup").get_active():
            self.dfile.set("StartupNotify", "true")
        else:
            self.dfile.set("StartupNotify", "false")

        self.dfile.set("Categories", categories)
        self.dfile.set("Comment" + LANG, comment)
        self.dfile.set("ShowOnlyIn", showonlyin)
        if not self.user_set_img:
            self.dfile.remove("Icon")

        self.dfile.save()

    def ok_pressed(self, num):
        if self.tree.get_object("ok").is_sensitive:
            self.save_desktop_file()
            self.destroy(0)

    def destroy(self, num):
        Gtk.main_quit()
