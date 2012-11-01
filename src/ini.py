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


class Ini(object):
    def __init__(self,path):
        self.path=path
        self.desktop_item={}
        self.read()
        
    def read(self):
        if os.path.isfile(self.path):
            f=open(self.path)
            lines=f.read().split("\n")
            f.close()
            for line in lines:
                l=line.split("=")
                if len(l)>1 and l[0]!="Encoding" l[0]!="Version" :
                    self.desktop_item.__setitem__(l[0],"=".join(l[1:]))
                    
    def get(self,key):
        if os.environ.has_key("LANG"):
            LANG=os.environ["LANG"][:5]
        else:
            LANG=""
        if self.desktop_item.has_key(key+"["+LANG+"]"):
            return self.desktop_item[key+"["+LANG+"]"]
        elif self.desktop_item.has_key(key+"["+LANG[:2]+"]"):
            return self.desktop_item[key+"["+LANG[:2]+"]"]
        elif self.desktop_item.has_key(key):
            return self.desktop_item[key]
        else:
            return ""
        
    def set(self,key,value):
        if len(value)>1:
            self.desktop_item.__setitem__(key,value)
        elif self.desktop_item.has_key(key):
            self.desktop_item.__delitem__(key)
    
    def remove(self,key):
        if self.desktop_item.has_key(key):
            self.desktop_item.__delitem__(key)
    
    def save(self):
        f=open(self.path,"w")
        f.write("#!/usr/bin/env xdg-open\n\n")
        f.write("[Desktop Entry]\n")
        f.write("Version=1.0\n")
        f.write("Encoding=UTF-8\n")
        keys=self.desktop_item.keys()
        keys.sort()
        f.write("Type="+self.desktop_item["Type"]+"\n")
        f.write("Name="+self.desktop_item["Name"]+"\n")
 
        for key in keys:
            if key not in ("Type", "Name"):
                f.write(key+"="+self.desktop_item[key]+"\n")
        f.close()
        os.system("chmod +x "+self.path)
        
