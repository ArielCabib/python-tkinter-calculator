#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Help.py
#       
#       Copyright 2010 Ariel Haviv <ariel.haviv@gmail.com>
#       
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
***The About window***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

from Tkinter import *
from xml.etree.ElementTree import ElementTree
ET = ElementTree()

class Help(Toplevel):
	def __init__(self, root):
		#initializing
		Toplevel.__init__(self)
		self.root = root
		self.protocol("WM_DELETE_WINDOW", self.withdraw)
		self.transient(root)
		self.title('Help')
		self.xml = ET.parse(self.root.global_file_help_xml)

		self.build_widgets(self)
		self.draw_widgets()
		self.set_init_layout()
		self.set_geometry(self)

	def build_widgets(self, root):
		self.title_lbl = Label(root, text = 'Python Calculator Help', font=('arial', 20))
		self.traceback_frm = Frame(root)
		self.tree_frm = Frame(root)
		self.text_lbl = Label(root, bg = 'white', relief = SUNKEN, justify = LEFT, wraplength=root.maxsize()[0]/3, font = ('arial', 10))
		self.back_btn = Button(root, text = 'Close', command = root.withdraw)

	def draw_widgets(self):
		self.title_lbl.grid(row=0, columnspan=2, pady=20, padx=20)
		self.traceback_frm.grid(row=1, columnspan=2, sticky=W, padx=10)
		self.tree_frm.grid(row=2, column=0, pady=10, padx=20, sticky=W)
		self.text_lbl.grid(row=2, column=1, padx=10, pady=10)
		self.back_btn.grid(row=3, columnspan=2, pady=20)

	def set_init_layout(self):
		#initializing layout
		self.traceback_btn = []
		self.tree_lbl = []
		self.current_nav_location = None
		self.nav_to(self.xml)

	def nav_to(self, elem):
		#navigate to the given XML element.
		if elem == self.current_nav_location: return #user clicked current subject. do nothing
		else: self.current_nav_location = elem #set new nav location

		self.delete_unneeded_btns(elem)
		self.refresh_labels(elem)
		self.refresh_text(elem)

	def delete_unneeded_btns(self, elem):
		#checking if there is any buttons to delete
		to_delete = 0
		for i in range(len(self.traceback_btn)):
			if self.traceback_btn[i].elem == elem:
				#found! setting 'to_delete' to one button ahead
				to_delete = i+1
				break
		if to_delete:
			while self.traceback_btn[to_delete:]:
				self.traceback_btn[to_delete].destroy()
				del (self.traceback_btn[to_delete])
		else:
			#user pressed a new subject. adding the button:
			self.traceback_btn.append(Button(self.traceback_frm, text=elem.attrib['title']))
			self.traceback_btn[-1].pack(side=LEFT)
			self.traceback_btn[-1].bind("<Button-1>", lambda e: self.nav_to(elem))
			self.traceback_btn[-1].elem = elem

	def refresh_labels(self, elem):
		#destroying current labels
		while self.tree_lbl:
			self.tree_lbl[0].destroy()
			del self.tree_lbl[0]

		#creating new ones
		for i in elem.getchildren():
			self.tree_lbl.append(Label(self.tree_frm, text=i.attrib['title'], font=('arial', 12)))
			self.tree_lbl[-1].elem = i #binding element to the label
			self.tree_lbl[-1].pack(anchor=W)
			self.tree_lbl[-1].bind("<Enter>", lambda e: e.widget.config(font=('arial', 12, 'bold')))
			self.tree_lbl[-1].bind("<Leave>", lambda e: e.widget.config(font=('arial', 12)))
			self.tree_lbl[-1].bind("<Button-1>", lambda e: self.nav_to(e.widget.elem))

	def refresh_text(self, elem):
		#refreshing explanation text
		self.text_lbl['text'] = elem.text

	def set_geometry(self, root):
		root.update_idletasks()
		w, h, (max_w, max_h) = root.winfo_width(), root.winfo_height(), root.maxsize()
		root.geometry("+%d+%d" % ((max_w-w)/2, (max_h-h)/2))
		
