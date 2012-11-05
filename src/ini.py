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
        self.desktop={}
        self.read()
        
    def read(self):
        if os.path.isfile(self.path):
            f=open(self.path)
            lines=f.read().split("\n")
            f.close()
            for line in lines:
                l=line.split("=")
                if len(l)==1 and not l[0].startswith("#"):# parse all entry [NAME]
                  entry=l[0]
                  self.desktop.__setitem__(entry,{})
                elif l[0]!="Encoding" and  l[0]!="Version" and not l[0].startswith("#"):# and add them to dictionary
                  self.desktop[entry].__setitem__(l[0],"=".join(l[1:]))
        else:
          self.desktop.__setitem__("[Desktop Entry]",{})
                    
    def get(self,key):
        dic=self.desktop["[Desktop Entry]"]
        if os.environ.has_key("LANG"):
            LANG=os.environ["LANG"][:5]
        else:
            LANG=""
        if dic.has_key(key+"["+LANG+"]"):
            return dic[key+"["+LANG+"]"]
        elif dic.has_key(key+"["+LANG[:2]+"]"):
            return dic[key+"["+LANG[:2]+"]"]
        elif dic.has_key(key):
            return dic[key]
        else:
            return ""
        
    def set(self,key,value):
        if len(value)>1:
            self.desktop["[Desktop Entry]"].__setitem__(key,value)
        elif self.desktop.has_key(key):
            self.desktop["[Desktop Entry]"].__delitem__(key)
    
    def remove(self,key):
        if self.desktop["[Desktop Entry]"].has_key(key):
            self.desktop["[Desktop Entry]"].__delitem__(key)
    
    def save(self):
        f=open(self.path,"w")
        f.write("#!/usr/bin/env xdg-open\n")
        #f.write("Version=1.0\n")
        #f.write("Encoding=UTF-8\n")
        entries=self.desktop.keys()
        for entry in entries:
          dic=self.desktop[entry]
          keys=dic.keys()
          keys.sort()
          f.write(entry+"\n")
          for key in keys:
             f.write(key+"="+dic[key]+"\n")

        f.close()
        os.system("chmod +x "+self.path)
        
