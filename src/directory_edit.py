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
import os,gettext,locale
from gi.repository import Gtk
from ini import Ini

class MainWindow(object):
    def __init__(self,data_dir,desktop_file_path,pkgname):
        self.file_path = data_dir
        self.dfile=Ini(desktop_file_path)

        gettext.bindtextdomain(pkgname, os.path.dirname(data_dir)+"/locale")
        gettext.textdomain(pkgname)
        locale.bind_textdomain_codeset(pkgname,'UTF-8')
        _ = gettext.gettext
        self._=_

        self.tree = Gtk.Builder()
        self.tree.set_translation_domain("light-desktop-item-edit")#doesn't work at all

        self.tree.add_from_file(os.path.join(self.file_path, 'directory-item-edit.ui'))
        self.user_set_img=False
        for obj in self.tree.get_objects():
          if obj.__gtype__==Gtk.Label.__gtype__ or obj.__gtype__==Gtk.CheckButton.__gtype__:
            obj.set_label(_(obj.get_label()))
        
        self.tree.get_object("dialog").set_title(_("Directory"))
        self.img=Gtk.Image()
        self.tree.get_object("icon-button").add(self.img)
        
        self.load_desktop_file()
        self.tree.get_object("ok").connect("released",self.ok_pressed)
        self.tree.get_object("cancel").connect("released",self.destroy)
        self.tree.get_object("name").connect("changed",self.name_changed)
        self.tree.get_object("icon-button").connect("released",self.icon_pressed)
        self.tree.get_object("icon-name").connect("changed",self.icon_name_changed)
        
        w=self.tree.get_object("dialog")
        w.show_all()
        Gtk.main()
    
    def icon_name_changed(self, n):
        text=self.tree.get_object("icon-name").get_text()
        self.dfile.set("Icon", text)
        self.user_set_img=False
        self.load_icon()
    
    def name_changed(self,w):
        text=self.tree.get_object("name").get_text()
        if  text.split(" ")[0].__len__()<1:
            self.user_set_img=False
            self.tree.get_object("ok").set_sensitive(False)
        else:
            self.tree.get_object("ok").set_sensitive(True)
        if  not self.user_set_img:
            self.tree.get_object("icon-name").set_text("")
            self.dfile.set("Icon", text.split(" ")[0].lower())
            self.load_icon()
    
    def icon_pressed(self, n):
        fc_dialog=Gtk.FileChooserDialog()
        
        filter=Gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        fc_dialog.add_filter(filter)
       
        fc_dialog.set_title(self._("Choose an icon..."))
        fc_dialog.set_current_folder(os.path.expanduser("~"))
        fc_dialog.set_action(Gtk.FileChooserAction.OPEN)
        fc_dialog.set_default_response(Gtk.ResponseType.OK)
        fc_dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)#,
        fc_dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        response=fc_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dfile.set("Icon", fc_dialog.get_filename())
            self.user_set_img=False
            self.load_icon()
        fc_dialog.destroy()
            
    def load_icon(self):
        if self.dfile.get("Icon").__contains__("/") and not self.user_set_img:
            self.img.set_from_file(self.dfile.get("Icon"))
            self.user_set_img=True
        else:
            icon=Gtk.IconTheme.get_default()
            try:
                pixbuf=icon.load_icon(self.dfile.get("Icon"), 48, 0)
                self.img.set_from_pixbuf(pixbuf)
                self.user_set_img=True
            except:
                if not self.user_set_img:
                    pixbuf=icon.load_icon("folder", 48, 0)
                    self.img.set_from_pixbuf(pixbuf)
            
    def load_desktop_file(self):
        LANG=""
        if os.environ.has_key("LANG"):
            LANG=os.environ["LANG"]
            if LANG[:2]=="en":
                LANG="["+LANG[:5]+"]"
            else:
                LANG="["+LANG[:2]+"]"
        
        print self.dfile.get("Name"+LANG)
        self.tree.get_object("name").set_text(self.dfile.get("Name"))
        self.tree.get_object("comment").set_text(self.dfile.get("Comment"))
        self.load_icon()
        
        
    def save_desktop_file(self):
        name=self.tree.get_object("name").get_text()
        comment=self.tree.get_object("comment").get_text()
        
        if os.environ.has_key("LANG"):
            LANG=os.environ["LANG"][:5]
            LANG="["+LANG+"]"
        else:
            LANG=""
        
        self.dfile.set("Name"+LANG, name)
        self.dfile.set("Name", name)
        self.dfile.set("Comment"+LANG, comment)
        self.dfile.set("Type","Directory")
        
        if not self.user_set_img:
            self.dfile.set("Icon","folder")
            
        self.dfile.save()

        
    def ok_pressed(self,num):
        if self.tree.get_object("ok").is_sensitive:
            self.save_desktop_file()
            self.destroy(0)
                    
    def destroy(self,num):
        Gtk.main_quit()
